from ipwhois.net import Net
from ipwhois.asn import IPASN
import sys
import threading
import whois
import dns.zone
import dns.resolver
import dns.reversename
import re


class Dnsquery:
    # import variables
    query_list = ["A", "AAAA", "NS", "MX", "TXT", "SOA"]
    mx_ip = []
    domain = []
    exchange = []
    ip_list = []
    srv_list = []
    o365 = 0
    ans = 0
    error = 0
    G = "\033[1;32;40m"
    R = "\033[1;31;40m"
    Y = "\033[1;33;40m"
    N = "\033[0m"
    mx_name = ''
    var = ''
    whois = ''

    def mail_ip(self):
        # find mail_server ip
        try:
            a = dns.resolver.resolve(self.mx_name, "A")
            for rdata in a:
                self.mx_ip = self.mx_ip + [rdata]
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NoNameservers:
            pass

    def mx_name_search(self):
        # choosing the mail_server with the highest priority
        try:
            m = dns.resolver.resolve(self.var, self.query_list[3])
            mx_list = []
            pref_list = []
            for rdata in m:
                mx = [rdata.exchange]
                pref = [rdata.preference]
                mx_list.extend(mx)
                pref_list.extend(pref)
            self.mx_name = str(mx_list[(pref_list.index(min(pref_list)))])
        except dns.resolver.NoAnswer:
            self.ans = 1
            print(self.R+"\nNo Email Service"+self.N)

    def compare(self):
        # compare mx_name with mail_list
        with open("mail_list.txt", "r", encoding="utf-8") as file_path:
            for count, line in enumerate(file_path):
                pass
        count += 1
        num = 0
        while num < count:
            if self.domain[num] in self.mx_name:
                self.ans = 1
                print(self.G+"Email Exchange Service"+self.N)
                print(self.exchange[num])
                if num == 3:
                    self.o365 = 1
                break
            else:
                num += 1

    def whois_mail(self):
        # running whois on mx_ip
        for num in range(len(self.mx_ip)):
            w = str(whois.whois(str(self.mx_ip[num])))
            with open("whois.txt", "w", encoding="utf-8") as blank:
                blank.write(w)
            with open("whois.txt", "r", encoding="utf-8") as read:
                lines = read.readlines()
                self.mx_name = lines[1].lower()
                self.compare()
            if self.ans == 1:
                break

    def record_search(self):
        # search for A, AAAA, NS, MX, TXT, SOA
        for num in range(len(self.query_list)):
            try:
                record = dns.resolver.resolve(self.var, self.query_list[num])
                print("\n"+self.G+self.query_list[num]+" Records"+self.N)
                for rdata in record:
                    print(rdata, "\n")
            except dns.resolver.NoAnswer:
                print(self.R+"\nNo "+self.query_list[num]+" Records"+self.N)
            except dns.resolver.NoNameservers:
                self.error = 1
                break
            except dns.resolver.NXDOMAIN:
                self.error = 1
                break
            except dns.resolver.LifetimeTimeout:
                self.error = 1
                break

    def list(self):
        # format srv_list
        with open("srvlist.txt", "r", encoding="utf-8") as f:
            for line in f:
                split = line.split()
                self.srv_list.extend(split)
        # format mail_list
        with open("mail_list.txt", "r", encoding="utf-8") as read:
            for line in read:
                split = line.split(" ")
                self.domain.extend([split[0]])
                self.exchange.extend([split[1]])

    def srv_tcp(self):
        # search for srv records with tcp
        for n in range(len(self.srv_list)):
            try:
                record = dns.resolver.resolve("_"+self.srv_list[n]+"._tcp."+self.var, "SRV")
                for data in record:
                    print(self.Y+"TCP:"+self.N, data)
            except dns.resolver.NXDOMAIN:
                pass
            except dns.exception.Timeout:
                pass
            except dns.resolver.NoAnswer:
                pass
            except dns.resolver.NoNameservers:
                pass

    def srv_tls(self):
        # search for srv records with tls
        for n in range(len(self.srv_list)):
            try:
                record = dns.resolver.resolve("_"+self.srv_list[n]+"._tls."+self.var, "SRV")
                for data in record:
                    print(self.Y+"TLS:"+self.N, data)
            except dns.resolver.NXDOMAIN:
                pass
            except dns.exception.Timeout:
                pass
            except dns.resolver.NoAnswer:
                pass
            except dns.resolver.NoNameservers:
                pass

    def srv_udp(self):
        # search for srv records with udp
        for n in range(len(self.srv_list)):
            try:
                record = dns.resolver.resolve("_"+self.srv_list[n]+"._udp."+self.var, "SRV")
                for data in record:
                    print(self.Y+"UDP:"+self.N, data)
            except dns.resolver.NXDOMAIN:
                pass
            except dns.exception.Timeout:
                pass
            except dns.resolver.NoAnswer:
                pass
            except dns.resolver.NoNameservers:
                pass

    def whois_ns_compare(self):
        # check if whois record is correct
        ans = 0
        self.whois = str(whois.whois(self.var)).lower()
        print(self.G+"\nComparing Whois name_server records"+self.N)
        try:
            record = dns.resolver.resolve(self.var, "NS")
            for rdata in record:
                pattern = str(rdata)
                if re.search(pattern, self.whois):
                    pass
                else:
                    ans = 1
                    print(self.R+"Whois name_server records misconfiguration"+self.N)
                    break
        except dns.resolver.NoAnswer:
            pass
        if ans == 0:
            print(self.Y+"Whois name_server records correct"+self.N)

    def ns_ip_compare(self):
        # check if ns are nested in same ip
        print(self.G+"\nEvaluating Name_Server IP"+self.N)
        try:
            ns = dns.resolver.resolve(self.var, "NS")
            ip_num = 0
            ip_set = set()
            for ns_data in ns:
                name = str(ns_data)
                a = dns.resolver.resolve(name, "A")
                for a_data in a:
                    string = re.sub(r".\d+$", "", str(a_data))
                    ip_set.add(string)
                    ip_num += 1
            if len(ip_set) != ip_num:
                print(self.R+"Name_Server nested in same IP\n"+self.N)
            else:
                print(self.Y+"Name_Server IP configuration correct\n"+self.N)
        except dns.resolver.NoAnswer:
            print(self.R+"No NS records to evaluate"+self.N)

    def xfr(self):
        master_addr = []
        print(self.G+"Attempting zone transfer for "+self.var+self.N)
        try:
            ns = dns.resolver.resolve(self.var, "NS")
            for ns_data in ns:
                a = dns.resolver.resolve(str(ns_data), "A")
                for a_data in a:
                    master_addr.append(str(a_data))
            for num in range(len(master_addr)):
                try:
                    xfr_answer = dns.query.xfr(master_addr[num], self.var)
                    zone = dns.zone.from_xfr(xfr_answer)
                    for name, ttl, rdata in zone.iterate_rdatas("A"):
                        print(self.Y+"A:"+self.N+str(name)+"."+self.var+self.Y+" | IP:"+self.N+str(rdata))
                    for name, ttl, rdata in zone.iterate_rdatas("MX"):
                        print(self.Y+"MX:"+self.N+str(rdata))
                    for name, ttl, rdata in zone.iterate_rdatas("TXT"):
                        print(self.Y+"TXT:"+self.N+str(rdata))
                    for name, ttl, rdata in zone.iterate_rdatas("CNAME"):
                        print(self.Y+"CNAME:"+self.N+str(name)+"."+self.var)
                    for name, ttl, rdata in zone.iterate_rdatas("SRV"):
                        print(self.Y+"SRV:"+self.N+str(name)+"."+self.var)
                except dns.query.TransferError:
                    print(self.R+master_addr[num]+" zone transfer failed"+self.N)
                except ConnectionResetError:
                    print(self.R+master_addr[num]+" zone transfer failed"+self.N)
                except dns.exception.FormError:
                    print(self.R+master_addr[num]+" zone transfer failed"+self.N)
                except TimeoutError:
                    print(self.R+master_addr[num]+" timed out"+self.N)
        except dns.resolver.NoNameservers:
            print(self.R+"No nameservers found"+self.N)
        except dns.resolver.NoAnswer:
            print(self.R+"No nameservers found"+self.N)

    def as_search(self):
        # ASN info search
        ip_list = set()
        try:
            ns = dns.resolver.resolve(self.var, "NS")
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
                print(self.G+"ASN info of "+self.N, ip_list[num])
                print(self.Y+" ASN:"+self.N, results['asn'], '|', self.Y+"Country:"+self.N, results['asn_country_code'], '|', self.Y+"ASN registry:"+self.N, results['asn_registry'].upper(), '|', self.Y+"Description:"+self.N, results['asn_description'])
        except dns.resolver.NoAnswer:
            print(self.R+"\nNo ASN records"+self.N)

    def regi_search(self):
        # registrar search
        print(self.G+"\nRegistrar "+self.N)
        with open("whois.txt", "w", encoding="utf-8") as f:
            f.write(self.whois)
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
                        print(regi.upper())
                        break
            except AttributeError:
                pass
        if ans != 1:
            print(self.R+"No registrar found \n"+self.N)

    def exp_date(self):
        # expiration date
        print(self.G+"Expiration date "+self.N)
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
                        print(exp)
                        break
                    else:
                        print(exp)
                        break
            except AttributeError:
                pass
            num += 1
        if ans != 1:
            print(self.R+"No Expiration date found "+self.N)

    def ptr(self):
        print(self.G+"PTR records"+self.N)
        try:
            addrs = dns.reversename.from_address(self.var)
            print(dns.resolver.resolve(str(addrs), "PTR")[0])
        except dns.resolver.NXDOMAIN:
            print(self.R+"No records found"+self.N)

    def o365check(self):
        print(self.G+"\nChecking if DNS records are configured for Office 365"+self.N)
        try:
            cname = dns.resolver.resolve("autodiscover."+self.var, "CNAME")
            for data in cname:
                if re.search("autodiscover\\.outlook\\.com", str(data)):
                    print(self.Y+"CNAME records have 'autodiscover.outlook.com'"+self.N+" (Office 365)")
                else:
                    print(self.R+"CNAME records not configured for Office 365"+self.N)
        except Exception:
            print(self.R+"CNAME records incorrect"+self.N)
        try:
            cname = dns.resolver.resolve("msoid."+self.var, "CNAME")
            for data in cname:
                if re.search("clientconfig\\.microsoftonline-p\\.net", str(data)):
                    print(self.Y+"CNAME records have 'clientconfig.microsoftonline-p.net'"+self.N+" (Office 365)")
                else:
                    pass
        except Exception:
            pass
        try:
            cname = dns.resolver.resolve("lyncdiscover."+self.var, "CNAME")
            for data in cname:
                if re.search("webdir\\.online\\.lync\\.com", str(data)):
                    print(self.Y+"CNAME records have 'webdir.online.lync.com'"+self.N+" (Skype)")
                else:
                    pass
        except Exception:
            pass
        try:
            ans = 0
            mx = dns.resolver.resolve(self.var, "MX")
            for data in mx:
                if re.search("mail\\.protection\\.outlook.com", str(data)):
                    print(self.Y+"MX records have 'mail.protection.outlook.com'"+self.N)
                    ans = 1
                    break
                elif re.search("protection\\.outlook.com", str(data)):
                    print(self.R+"MX record deprecated, please update to 'mail.protection.outlook.com'"+self.N)
                    ans = 1
                    break
                else:
                    pass
            if ans != 1:
                print(self.R+"MX records not configured for Office 365"+self.N)
        except Exception:
            print(self.R+"MX records incorrect"+self.N)
        try:
            ans = 0
            spf = dns.resolver.resolve(self.var, "txt")
            for data in spf:
                if re.search("include:spf\\.protection\\.outlook.com", str(data)):
                    print(self.Y+"SPF records have 'include:spf.protection.outlook.com'"+self.N)
                    ans = 1
                    break
                else:
                    pass
            if ans != 1:
                print(self.R+"SPF records not configured for Office 365"+self.N)
        except Exception:
            print(self.R+"SPF records incorrect"+self.N)
        try:
            tls = dns.resolver.resolve("_sip._tls."+self.var, "SRV")
            if tls:
                print(self.Y+"SRV records have 'sipdir.online.lync.com'"+self.N)
        except Exception:
            print(self.R+"SRV records doesn't have sipdir.online.lync.com"+self.N)
        try:
            tcp = dns.resolver.resolve("_sipfederationtls._tcp."+self.var, "SRV")
            if tcp:
                print(self.Y+"SRV records have 'sipfed.online.lync.com"+self.N)
        except Exception:
            print(self.R+"SRV records doesn't have sipfed.online.lync.com"+self.N)

    def www_check(self):
        print(self.G+"\nChecking for www record"+self.N)
        try:
            a = dns.resolver.resolve("www."+self.var, "A")
            if a:
                print(self.Y+"Domain have www record: "+self.N+"www."+self.var+"\n")
        except Exception:
            print(self.R+"Domain doesn't have www record\n"+self.N)


def query(var, query_type):
    run = Dnsquery()
    run.var = var
    run.list()
    if query_type == "std":
        run.record_search()
        if run.error != 1:
            run.whois_ns_compare()
            run.ns_ip_compare()
            run.as_search()
            run.regi_search()
            run.exp_date()
            run.www_check()
            run.mx_name_search()
            run.mail_ip()
            run.compare()
            if run.ans != 1:
                run.whois_mail()
                if run.ans != 1:
                    print(run.G+"\nEmail Exchange Service"+run.N)
                    print(run.R+"No Email Service in Database\n"+run.N)
            if run.o365 == 1:
                run.o365check()
        else:
            print(run.R+"\nDomain does not exist"+run.N)
    elif query_type == "all":
        run.record_search()
        if run.error != 1:
            run.whois_ns_compare()
            run.ns_ip_compare()
            run.as_search()
            run.regi_search()
            run.exp_date()
            run.mx_name_search()
            run.mail_ip()
            run.compare()
            if run.ans != 1:
                run.whois_mail()
                if run.ans != 1:
                    print(run.G+"\nEmail Exchange Service"+run.N)
                    print(run.R+"No Email Service in Database\n"+run.N)
            if run.error == 1:
                pass
            else:
                print(run.G+"Brute forcing SRV Records, this may take awhile..."+run.N)
                if __name__ == "dnsquery":
                    p1 = threading.Thread(target=run.srv_tcp)
                    p1.start()
                    p2 = threading.Thread(target=run.srv_tls)
                    p2.start()
                    p3 = threading.Thread(target=run.srv_udp)
                    p3.start()
                    p1.join()
                    p2.join()
                    p3.join()
        else:
            print(run.R+"\nDomain does not exist"+run.N)
        print(run.G+"Finished query\n"+run.N)
        sys.exit()
    elif query_type == "srv":
        print(run.G+"Brute forcing SRV Records, this may take awhile..."+run.N)
        if __name__ == "dnsquery":
            p4 = threading.Thread(target=run.srv_tcp)
            p4.start()
            p5 = threading.Thread(target=run.srv_tls)
            p5.start()
            p6 = threading.Thread(target=run.srv_udp)
            p6.start()
            p4.join()
            p5.join()
            p6.join()
        print(run.G+"Finished query\n"+run.N)
        sys.exit()
    elif query_type == "mail":
        run.mx_name_search()
        run.mail_ip()
        run.compare()
        if run.ans != 1:
            run.whois_mail()
            if run.ans != 1:
                print(run.G+"\nEmail Exchange Service"+run.N)
                print(run.R+"No Email Service in Database\n"+run.N)
    elif query_type == "reg":
        run.whois = str(whois.whois(run.var)).lower()
        run.regi_search()
    elif query_type == "exp":
        run.whois = str(whois.whois(run.var)).lower()
        run.exp_date()
    elif query_type == "asn":
        run.as_search()
    elif query_type == "eva":
        run.whois_ns_compare()
        run.ns_ip_compare()
    elif query_type == "ptr":
        run.ptr()
    elif query_type == "xfr":
        run.xfr()
    elif query_type == "365":
        run.o365check()
    print(run.G+"\nFinished query\n"+run.N)
