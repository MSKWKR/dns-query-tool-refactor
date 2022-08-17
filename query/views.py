from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from ipwhois.net import Net
from ipwhois.asn import IPASN
import sys
import threading
import whois
import dns.zone
import dns.resolver
import dns.reversename
import re
import sqlite3
from datetime import datetime, timezone
import pytz
from sqlite3 import Error


# Create your views here.
def index(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))
def search(request):
    global domain
    try:
        domain = request.POST["domain"]
    except Exception:
        pass
    template = loader.get_template('ans.html')
    try:
        dns.resolver.resolve(domain, "A")
    except dns.resolver.NXDOMAIN:
        sys.exit()
    except dns.resolver.NoAnswer:
        pass

    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_record(conn, domain, records):
        sql = ''' INSERT INTO '''+domain+''' (record_type, record_value)
                  VALUES(?,?) '''
        cur = conn.cursor()
        try:
            cur.execute(sql, records)
            conn.commit()
        except Error as e:
            print(e)

    def main():
        database = "query.db"
        domain2 = record_search("domain")
        sql_create_domain_table = """ CREATE TABLE IF NOT EXISTS """+domain2+""" (
                                                record_type text,
                                                record_value text
                                            ); """
        # create a database connection
        conn = create_connection(database)
        if soa_check(domain2) == "same":
            print("same")
        else:
            with conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute('drop table '+domain2)
                except Exception:
                    pass
                create_table(conn, sql_create_domain_table)
                # trivial records
                type = ["A", "AAAA", "NS", "MX", "TXT", "SOA"]
                for x in type:
                    for num in range(len(record_search(x))):
                        records = (x, record_search(x)[num])
                        create_record(conn, domain2, records)
                # whois
                w = str(whois.whois(domain)).lower()
                records = ("whois", w)
                create_record(conn, domain2, records)
                # asn
                type = ["ip", "asn", "country", "registry", "description"]
                for x in type:
                    for num in range(len(as_search(x))):
                        records = (x , as_search(x)[num])
                        create_record(conn , domain2, records)

    def record_search(type):
        domain2 = re.sub("\\.","_", domain)
        domain2 = re.sub(r"-", "_", domain2)
        if re.search(r"^[0-9]", domain2):
            domain2 = str("_"+domain2)
        record = []
        if type == "domain":
            return domain2
        else:
            try:
                q = dns.resolver.resolve(domain, type)
                for data in q:
                    record.append(str(data))
            except Exception:
                record.append("none")
            return record

    def soa_check(domain2):
        conn = sqlite3.connect("query.db")
        try:
            q = dns.resolver.resolve(domain, "SOA")
            for data in q:
                serial = data.serial
        except Exception:
            return "none"
        cursor = conn.cursor()
        try:
            cursor.execute('select record_value from '+domain2+' where record_type="SOA"')
            result = cursor.fetchall()
        except Exception:
            return "none"
        if serial:
            if re.search(str(serial), str(result)):
                return "same"

    def database_search(type):
        result = []
        domain2 = record_search("domain")
        conn = sqlite3.connect("query.db")
        cursor = conn.cursor()
        cursor.execute('select record_value from '+domain2+' where record_type="'+type+'"')
        tempresult = cursor.fetchall()
        cursor.close()
        for row in tempresult:
            if str(row[0]) == "none":
                return "none"
            else:
                result.append(row[0])
        return result

    def whois_ns_compare():
        error = "false"
        domain2 = record_search("domain")
        conn = sqlite3.connect("query.db")
        cursor = conn.cursor()
        cursor.execute('select record_value from '+domain2+' where record_type="whois"')
        result = cursor.fetchall()
        cursor.close()
        for row in result:
            w = row[0]
        try:
            record = dns.resolver.resolve(domain, "NS")
            for data in record:
                pattern = str(data)
                if re.search(pattern, w):
                    pass
                else:
                    error = "true"
                    return "misconfigured"
        except Exception:
            return "misconfigured"
        if error == "false":
            return "correct"

    def ns_ip_compare():
        domain2 = record_search("domain")
        conn = sqlite3.connect("query.db")
        cursor = conn.cursor()
        cursor.execute('select record_value from '+domain2+' where record_type="NS"')
        result = cursor.fetchall()
        cursor.close()
        ns = []
        for row in result:
             ns.append(row[0])
        try:
            ip_num = 0
            ip_set = set()
            for name in ns:
                a = dns.resolver.resolve(name, "A")
                for a_data in a:
                    string = re.sub(r".\d+$", "", str(a_data))
                    ip_set.add(string)
                    ip_num += 1
            if len(ip_set) != ip_num:
                return "misconfigured"
            else:
                return "correct"
        except Exception:
            return "none"

    def as_search(type):
        ip_list = set()
        asn_list = []
        country = []
        registry = []
        description = []
        try:
            ns = dns.resolver.resolve(domain, "NS")
            for ns_data in ns:
                name = str(ns_data)
                a = dns.resolver.resolve(name, "A")
                for a_data in a:
                    ip_list.add(str(a_data))
            ip_list = list(ip_list)
            for num in range(len(ip_list)):
                net = Net(ip_list[num])
                obj = IPASN(net)
                results = obj.lookup()
                asn_list.append(results['asn'])
                country.append(results['asn_country_code'])
                registry.append(results['asn_registry'])
                description.append(results['asn_description'])

        except Exception:
            return "none"
        if type == "ip":
            return ip_list
        if type == "asn":
            return asn_list
        if type == "country":
            return country
        if type == "registry":
            return registry
        if type == "description":
            return description

    def regi_search():
        domain2 = record_search("domain")
        conn = sqlite3.connect("query.db")
        cursor = conn.cursor()
        cursor.execute('select record_value from '+domain2+' where record_type="whois"')
        result = cursor.fetchall()
        cursor.close()
        for row in result:
            w = row[0]
        with open("whois.txt", "w", encoding="utf-8") as f:
            f.write(w)
        with open("whois.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            ans = 0
        for num in range(len(lines)):
            try:
                x = re.search(r"\bregistrar\b", (lines[num])).groups()
                if x == ():
                    regi = re.sub(r'( "registrar": )', '', lines[num])
                    regi = re.sub(r",", '', regi)
                    try:
                        re.search("null", regi).groups()
                        break
                    except AttributeError:
                        ans = 1
                        return regi.upper()
            except AttributeError:
                pass
        if ans != 1:
            return "none"

    def exp_date():
        with open("whois.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            num = 0
            ans = 0
        while num < len(lines):
            try:
                x = re.search(r"\bexpiration_date\b", (lines[num])).groups()
                if x == ():
                    exp = re.sub(r'( "expiration_date": )', '', lines[num])
                    exp = re.sub(r",", '', exp)
                    try:
                        re.search("null", exp).groups()
                        break
                    except AttributeError:
                        ans = 1
                    if "[" in exp:
                        num += 1
                        exp = re.sub(r'^\s*', '', lines[num])
                        exp = re.sub(r",", '', exp)
                        return exp
                    else:
                        return exp
            except AttributeError:
                pass
            num += 1
        if ans != 1:
            return "none"

    def o365check(type):
        if type == "auto":
            try:
                cname = dns.resolver.resolve("autodiscover."+domain, "CNAME")
                for data in cname:
                    if re.search(r"autodiscover.outlook.com", str(data)):
                        return "correct"
                    else:
                        return "misconfigured"
            except Exception:
                return "misconfigured"
        if type == "msoid":
            try:
                cname = dns.resolver.resolve("msoid."+domain, "CNAME")
                for data in cname:
                    if re.search(r"clientconfig.microsoftonline-p.net", str(data)):
                        return "correct"
                    else:
                        pass
            except Exception:
                pass
        if type == "lync":
            try:
                cname = dns.resolver.resolve("lyncdiscover."+domain, "CNAME")
                for data in cname:
                    if re.search(r"webdir.online.lync.com", str(data)):
                        return "correct"
                    else:
                        pass
            except Exception:
                pass
        if type == "365mx":
            try:
                ans = 0
                mx = dns.resolver.resolve(domain, "MX")
                for data in mx:
                    if re.search(r"mail.protection.outlook.com", str(data)):
                        ans = 1
                        return "correct"
                        break
                    elif re.search(r"protection.outlook.com", str(data)):
                        ans = 1
                        return "update"
                        break
                    else:
                        pass
                if ans != 1:
                    return "misconfigured"
            except Exception:
                return "misconfigured"
        if type == "spf":
            try:
                ans = 0
                spf = dns.resolver.resolve(domain, "txt")
                for data in spf:
                    if re.search(r"include:spf.protection.outlook.com", str(data)):
                        ans = 1
                        return "correct"
                        break
                    else:
                        pass
                if ans != 1:
                    return "misconfigured"
            except Exception:
                return "misconfigured"
        if type == "sipdir":
            try:
                tls = dns.resolver.resolve("_sip._tls."+domain, "SRV")
                if tls:
                    return "correct"
            except Exception:
                return "misconfigured"
        if type == "sipfed":
            try:
                tcp = dns.resolver.resolve("_sipfederationtls._tcp."+domain, "SRV")
                if tcp:
                    return "correct"
            except Exception:
                return "misconfigured"

    def mail_search(type):
        domain_exchange = []
        exchange_list = []
        ans = 0
        if type == "search":
            with open("mail_list.txt", "r", encoding="utf-8") as read:
                for line in read:
                    split = line.split(" ")
                    domain_exchange.extend([split[0]])
                    exchange_list.extend([split[1]])
            try:
                m = dns.resolver.resolve(domain, "MX")
                mx_list = []
                pref_list = []
                for rdata in m:
                    mx = [rdata.exchange]
                    pref = [rdata.preference]
                    mx_list.extend(mx)
                    pref_list.extend(pref)
                mx_name = str(mx_list[(pref_list.index(min(pref_list)))])
            except dns.resolver.NoAnswer:
                return "misconfigured"
            with open("mail_list.txt", "r", encoding="utf-8") as file_path:
                for count, line in enumerate(file_path):
                    pass
            count += 1
            num = 0
            while num < count:
                if domain_exchange[num] in mx_name:
                    ans = 1
                    if num == 3:
                        return "Office_365"
                    elif num == 1 :
                        return "Gmail"
                    elif num == 2 :
                        return "Gmail"
                    elif num == 0:
                        return "Google_Workspace"
                    elif num == 5:
                        return "Amazon_SES"
                    elif num == 6:
                        return "Yahoo!_Mail"
                    return exchange_list[num]
                else:
                    num += 1
            if ans == 0:
                return "misconfigured"


    def www_check():
        try:
            a = dns.resolver.resolve("www."+domain, "A")
            if a:
                return "correct"
        except Exception:
            return "none"
    time = datetime.now(pytz.timezone("Asia/Taipei"))
    main()
    context = {
        "domain": domain,
        "a": database_search("A"),
        "aaaa": database_search("AAAA"),
        "ns": database_search("NS"),
        "mx": database_search("MX"),
        "txt": database_search("TXT"),
        "soa": database_search("SOA"),
        "whois_ns": whois_ns_compare(),
        "ns_ip": ns_ip_compare(),
        "ip": database_search("ip"),
        "asn": database_search("asn"),
        "country": database_search("country"),
        "registry": database_search("registry"),
        "description": database_search("description"),
        "registrar": regi_search(),
        "exp_date": exp_date(),
        "auto": o365check("auto"),
        "msoid": o365check("msoid"),
        "lync": o365check("lync"),
        "365mx": o365check("365mx"),
        "spf": o365check("spf"),
        "sipdir": o365check("sipdir"),
        "sipfed": o365check("sipfed"),
        "mail_search": mail_search("search"),
        "www": www_check(),
        "wans": "http://www."+domain,
        "time": time.strftime('%Y/%m/%d %H:%M:%S'),
        "mode": 1,

    }
    return HttpResponse(template.render(context, request))

def whoisdetails(request):
    global domain
    ns_ans = []
    missing = []
    whoishtml = []
    template = loader.get_template('whois.html')
    with open("whois.txt", "r", encoding="utf-8") as w:
        for lines in w:
            lines = re.sub(r"\\n", "", lines)
            lines = re.sub(r"^{", "", lines)
            lines = re.sub(r"}$", "", lines)
            whoishtml.append(lines.lower())
        whoistxt = str(w.read())
    ns = dns.resolver.resolve(domain, "NS")
    for data in ns:
        ns_ans.append(str(data))
    def quicktest():
        error = "false"
        for num in range(len(ns_ans)):
            if re.search(ns_ans[num], str(whoishtml)):
                pass
            else:
                error = "true"
                missing.append(ns_ans[num])
        if error == "true":
            return "error"
        elif error == "false":
            return "correct"
    context = {
        "whoistxt": whoishtml,
        "ns": ns_ans,
        "domain": domain,
        "missing": missing,
        "check": quicktest(),
    }
    return HttpResponse(template.render(context, request))

def nsdetails(request):
    global domain
    ns_data = []
    ip_data = []
    check = []
    duplist = set()
    space = []
    template = loader.get_template('ns.html')
    ns = dns.resolver.resolve(domain, "NS")
    for data in ns:
        ns_data.append(str(data))
    for num in range(len(ns_data)):
        ip = dns.resolver.resolve(ns_data[num], "A")
        ip_data.append("IP of "+ns_data[num]+" :")
        for data in ip:
            ip_data.append(str(data))
            string = re.sub(r".\d+$", "", str(data))
            check.append(string)
    for x in check:
        if x not in space :
            space.append(x)
        else:
            duplist.add(x)
    def quicktest():
        if len(duplist) != 0:
            return "error"
        else:
            return "correct"

    context = {
        "ip": ip_data,
        "duplicates": duplist,
        "check": quicktest(),
    }
    return HttpResponse(template.render(context, request))

