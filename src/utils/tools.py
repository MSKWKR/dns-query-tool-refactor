"""DNS Tool Box"""
import concurrent.futures
import datetime
import http.client
import re
import socket
import time
from typing import Optional, List
from urllib.parse import urlparse

import dns.exception
import dns.resolver
import dns.zone
import pytz as pytz
import tld
import whois
from ipwhois.asn import IPASN
from ipwhois.net import Net

from src.utils.log.log import exception, LOGGER
from .blacklist_checker import BlackListChecker
from .constants import EMAIL_TABLE, SRV_LIST
from .valid_result import Validator

ToolBoxErrors = (
    ValueError, TypeError, EOFError, ConnectionResetError, TimeoutError, dns.exception.FormError,
    dns.exception.SyntaxError, dns.exception.UnexpectedEnd, dns.exception.TooBig, dns.exception.Timeout,
    dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.YXDOMAIN,
    dns.query.TransferError, dns.name.EmptyLabel, socket.error
)


class DNSToolBox:
    """
    DNSToolBox is a generic-style set that contains the methods needed to check the domain string
    """

    # the tool is defaulted with nothing
    def __init__(self):
        """Initializes class attribute"""
        self.check_time = None

        self._domain_string = None
        self._res = dns.resolver.Resolver()
        self._black_list_checker = BlackListChecker()
        self._validator = Validator()

    def __repr__(self):
        return f"DNSToolBox{self._domain_string}"

    # ------------------------- Helper Function ------------------------------------
    @classmethod
    @exception(LOGGER)
    def strip_last_dot(cls, addr: str) -> str:
        """
        Util function that strips the last dot from an address (if any)

        :param addr: The Address returned by search
        :type: str

        :return: The adjusted address
        :rtype: str
        """
        return addr[:-1] if addr.endswith('.') else addr

    @classmethod
    @exception(LOGGER)
    def parse_raw_domain(cls, input_domain: str) -> Optional[str]:
        """
        Method parse_raw_domain cleanses the input domain and return the domain name

        :param input_domain: Raw input domain, might have error key-in symbols
        :type: str

        :return: The cleansed domain string
        :rtype: str
        """

        pattern = '[^A-Za-z0-9.:/]'
        input_domain = re.sub(pattern=pattern, repl="", string=input_domain).lower()
        try:
            # fixing protocol means the protocol we use now is http and https, ftp will fail
            input_domain = tld.get_fld(input_domain, fix_protocol=True)
        except (tld.exceptions.TldBadUrl, tld.exceptions.TldDomainNotFound) as error:
            # print(f"{error=}")
            LOGGER.exception(msg=f"Domain Parse Error: {error}")
            input_domain = None
        return input_domain

    @exception(LOGGER)
    def set_domain_string(self, domain_string: str) -> str:
        """
        Set_domain_string parses, initialize and return the pure domain string

        :param domain_string: The original input string(unparsed)
        :type: str

        :return: The parsed, usable domain
        :rtype: str
        """

        self._domain_string = DNSToolBox.parse_raw_domain(domain_string)

        return self._domain_string

    # ------------------------- Search Tools ------------------------------------
    @exception(LOGGER)
    def search(self, record_type: str) -> Optional[dns.resolver.Resolver]:
        """
        The method search with the record type is a generic function
        that wraps the search of the given record type and the exceptions.

        :param record_type: The specific type we want to search for the domain
        :type: str

        :return: The answers by searching the given url with A Record type, None if not found
        :rtype dns.resolver.Resolver or None
        """
        try:
            return self._res.resolve(self._domain_string, record_type)
        # Return None when input domain is incorrect
        except ToolBoxErrors as error:
            LOGGER.exception(msg=f"DNS Record Error: {error}")
            # print(f"{error=}")
            return None

    @exception(LOGGER)
    def search_www(self) -> Optional[dns.resolver.Resolver]:
        """
        Search_www check www domain by checking it's A Record.

        :return: The answers by searching the given url with A Record type, None if not found
        :rtype dns.resolver.Resolver or None
        """
        try:
            # this shouldn't be the correct way, what if my input domain is 'www.example.com'?
            # would cause an error
            answers = self._res.resolve("www." + self._domain_string, "A")
            if answers:
                return answers

        except ToolBoxErrors as error:
            LOGGER.exception(msg=f"DNS Record Error: {error}")
            # print(f"{error=}")
        return None

    @exception(LOGGER)
    def search_whois(self) -> any:
        """
        Query a WHOIS server directly and return the parsed whois data.

        :return: The result for parsing the WHOIS data, None if not found
        :rtype whois.parser.WhoisTw, None
        """
        try:
            whois_result = whois.whois(self._domain_string)
            return whois_result
        # Handle TypeError by returning None
        except ToolBoxErrors as error:
            LOGGER.exception(msg=f"DNS Record Error: {error}")
            # print(f"{error=}")
            return None

    @classmethod
    @exception(LOGGER)
    def search_ipwhois_asn(cls, ip_address: str) -> dict[any:any]:
        """
        Util function that searches the ASN records with the given IP

        :param ip_address: An IPv4 or IPv6 string
        :type: str

        :return: An ASN dictionary after parsing with the given ip address,
                 returns an empty dictionary if not found
        :rtype: dict
        """
        # default an empty dictionary
        asn_results = dict()
        try:
            # net is the object for performing network queries
            net = Net(ip_address)
            # IPASN is the class for parsing ASN data for an ip address
            object_ = IPASN(net)
            asn_results = object_.lookup(ip_address)
            return asn_results

        # Catches ValueError when ip isn't correct
        except ToolBoxErrors as error:
            LOGGER.exception(msg=f"DNS Record Error: {error}")
            # print(f"{error=}")
            return asn_results

    @exception(LOGGER)
    def search_o365(self, record_type: str) -> Optional[dns.resolver.Resolver]:
        """
        The method search_o365 with record type is a generic function
        that wraps the search of the given record type and the exceptions.

        :param record_type: The specific o365 record type we want to search for the domain
        :type: str

        :return: The answers by searching the given url with A Record type, None if not found
        :rtype dns.resolver.Resolver or None
        """
        answers = None
        try:
            match record_type:
                case "auto":
                    answers = dns.resolver.resolve(f"autodiscover.{self._domain_string}", "CNAME")

                case "msoid":
                    answers = dns.resolver.resolve(f"msoid.{self._domain_string}", "CNAME")

                case "lync":
                    answers = dns.resolver.resolve(f"lyncdiscover.{self._domain_string}", "CNAME")

                case "365mx":
                    answers = dns.resolver.resolve(self._domain_string, "MX")

                case "spf":
                    answers = dns.resolver.resolve(self._domain_string, "txt")

                case "sipdir":
                    answers = dns.resolver.resolve(f"_sip._tls.{self._domain_string}", "SRV")

                case "sipfed":
                    answers = dns.resolver.resolve(f"_sipfederationtls._tcp.{self._domain_string}", "SRV")

                case _:
                    raise NameError(f"o365 Record Type Input Error: {record_type}")

        except ToolBoxErrors as error:
            LOGGER.exception(msg=f"DNS Record Error: {error}")
            # print(f"{error=}")

        return answers

    # ------------------------- Get Result Tools ------------------------------------
    @exception(LOGGER)
    def get_srv_results(self, proto="tcp") -> List[str]:
        """
            Util function for searching srv records for with the given protocol name, default to tcp.

            :return: The searched srv records
            :rtype: List[str]
        """
        srv = "SRV"

        proto = proto.lower()
        srv_result_list = []
        for n in range(len(SRV_LIST)):
            try:
                srv_record = dns.resolver.resolve(f"_{SRV_LIST[n]}._{proto}.{self._domain_string}", srv)
                for data in srv_record:
                    srv_result = data.to_text()
                    if self._validator.is_valid(self._domain_string, srv, srv_result):
                        srv_result_list.append(srv_result)

            except ToolBoxErrors as error:
                # Not logging it since parsing the srv list is too much
                # LOGGER.exception(msg=f"SRV Record Error: {error}")
                # print(f"{error=}")
                pass
        return srv_result_list

    @exception(LOGGER)
    def get_result(self, record_type: str) -> str | List[str]:
        """
        Function for getting the asked Record Type.
        Can accept input Record type 'A', 'AAAA', 'NS', 'MX', 'TXT', 'SOA', 'WWW' with its upper and lower cases.
        Return an empty string or empty list if input record type is incorrect or the domain itself malfunctioned.

        :param record_type: DNS record type
        :type record_type: str

        :return: The transformed search result
        :rtype: str, List
        """

        record_type = record_type.upper()
        match record_type:
            case ("A" | "AAAA" | "SOA" | "MX"):
                answers = self.search(record_type)

                result = ""
                if answers:
                    # answers is an iterator of type records, need to loop through in order to get the data
                    for answer in answers:
                        # answer is a dns.resolver.Answer instance, return type should be a converted string
                        result = str(answer)
                        if not self._validator.is_valid(self._domain_string, record_type, result):
                            # return an empty result if the given answer is incorrect
                            LOGGER.exception(msg=f"DNS Record Invalid: {result}")
                            # print(f"Incorrect result: {result}")
                            return ""
                        return result
                else:
                    return result

            case "TXT":
                answers = self.search(record_type)
                txt_result = []
                if answers:
                    for answer in answers:
                        txt_result.append(str(answer))
                return txt_result

            case "NS":
                answers = self.search(record_type)
                ns_result = []
                if answers:
                    for answer in answers:
                        ns = self.strip_last_dot(answer.target.to_text())
                        ns_result.append(ns)
                return ns_result

            case ("IPV4" | "IPV6"):
                a_request_type = "A" if record_type == "IPV4" else "AAAA"
                ns_list = self.get_result("NS")
                ip_list = []
                for ns_data in ns_list:
                    name = str(ns_data)
                    try:
                        a = dns.resolver.resolve(name, a_request_type)
                        for a_data in a:
                            # check whether ip is valid first
                            a_result = str(a_data)
                            if not self._validator.is_valid(self._domain_string, a_request_type, a_result):
                                LOGGER.exception(msg=f"DNS Record Invalid: {a_result}")
                            ip_list.append(a_result)

                    except ToolBoxErrors as error:
                        LOGGER.exception(msg=f"DNS Record Error: {error}")
                        # print(f"{error=}")
                return ip_list

            case "WWW":
                answers = self.search_www()
                return f"www.{self._domain_string}" if answers else ""

            case _:
                raise NameError(f"Record Type Input Error: {record_type}")

    @exception(LOGGER)
    def get_o365_result(self, record_type: str) -> str:
        """
        Util for checking if the o365 record type exists.

        :param record_type: o365 record type
        :type: str

        :return: True if record type exists else False
        :rtype: bool
        """

        answers = self.search_o365(record_type)
        o365_pattern_dict = {
            # o365 type, regex pattern
            "auto": "autodiscover.outlook.com",
            "msoid": "clientconfig.microsoftonline-p.net",
            "lync": "webdir.online.lync.com",
            "365mx": ("mail.protection.outlook.com", "protection.outlook.com"),
            "spf": "include:spf.protection.outlook.com",
            "sipdir": "sipdir.online.lync.com",
            "sipfed": "sipfed.online.lync.com"
        }

        match record_type:

            case "auto" | "msoid" | "lync" | "spf" | "sipdir" | "sipfed":
                if answers:
                    for answer in answers:
                        if re.search(rf"{o365_pattern_dict[record_type]}", str(answer)):
                            return o365_pattern_dict[record_type]

            case "365mx":
                if answers:
                    for answer in answers:
                        if re.search(rf"{o365_pattern_dict[record_type][0]}", str(answer)) or \
                                re.search(rf"{o365_pattern_dict[record_type][1]}", str(answer)):
                            return o365_pattern_dict[record_type][0] or o365_pattern_dict[record_type][1]

        return ""

    # ---------------------------------------------- ToolBox Features -----------------------------------------
    @exception(LOGGER)
    def o365_results(self) -> dict[str: List[str]]:
        o365_types = ["auto", "msoid", "lync", "365mx", "spf", "sipdir", "sipfed"]
        o365_results_dict = {
            "CNAME": [],
            "MX": [],
            "SPF": [],
            "SRV": []
        }
        for o365_type in o365_types:
            o365_result = self.get_o365_result(o365_type)

            match o365_type:
                case "auto" | "msoid" | "lync":
                    o365_results_dict["CNAME"].append(o365_result)
                case "365mx":
                    o365_results_dict["MX"].append(o365_result)
                case "spf":
                    o365_results_dict["SPF"].append(o365_result)
                case "sipdir" | "sipfed":
                    o365_results_dict["SRV"].append(o365_result)

        return o365_results_dict

    # Since the tool wants the specific field for the ASN,
    # this is dirty code that I didn't change much
    @exception(LOGGER)
    def asn(self) -> dict[str:List[str]]:
        """
        Function for reading the ASN result parsed from search_ipwhois_asn(),
        will leave all the fields empty if the ip list is empty

        :return: The required ASN fields
        :rtype: dict
        """
        ip_list = self.get_result("ipv4")
        asn_list = []
        country_list = []
        registry_list = []
        description_list = []

        # Default the fields key
        asn_dict = dict.fromkeys(['ip_list', 'asn_list', 'country_list', 'registry_list', 'description_list'])
        for ip in ip_list:
            asn_result = self.search_ipwhois_asn(ip)
            asn = asn_result['asn']
            country = asn_result['asn_country_code']
            registry = asn_result['asn_registry']
            description = asn_result['asn_description']

            asn_list.append(asn)
            country_list.append(country)
            registry_list.append(registry)
            description_list.append(description)

        # assign the lists to its specific field
        asn_dict['ip_list'] = ip_list
        asn_dict['asn_list'] = asn_list
        asn_dict['country_list'] = country_list
        asn_dict['registry_list'] = registry_list
        asn_dict['description_list'] = description_list

        return asn_dict

    @exception(LOGGER)
    def srv(self) -> dict[str: List[str]]:
        """
        Util for getting the srv record for the searched domain

        :return: The dictionary for the SRV records with field udp, tcp and tls
        :rtype: dict
        """

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            srv_udp_result = executor.submit(self.get_srv_results, "udp").result()
            srv_tcp_result = executor.submit(self.get_srv_results, "tcp").result()
            srv_tls_result = executor.submit(self.get_srv_results, "tls").result()

        srv_result_dict = {
            "UDP": srv_udp_result,
            "TCP": srv_tcp_result,
            "TLS": srv_tls_result
        }

        return srv_result_dict

    @exception(LOGGER)
    def xfr(self) -> List[str]:
        xfr_list = []
        try:
            soa_answer = self.search("soa")
            if soa_answer:
                master_answer = dns.resolver.resolve(soa_answer[0].mname, "A")
                zone = dns.zone.from_xfr(dns.query.xfr(master_answer[0].address, self._domain_string))
                for n in sorted(zone.nodes.keys()):
                    xfr_list.append(zone[n].to_text(n))
        except ToolBoxErrors as error:
            LOGGER.exception(msg=f"DNS XFR Record Error: {error}")
            # print(f"{error=}")

        return xfr_list

    @exception(LOGGER)
    def ptr(self) -> str:
        """
        Util function for getting the ptr record using reverse query

        :return: The PTR record
        """
        try:
            address = dns.reversename.from_address(self.get_result("a"))
            return str(dns.resolver.resolve(str(address), "PTR")[0])
        except ToolBoxErrors as error:
            LOGGER.exception(msg=f"DNS PTR Record Error: {error}")
            # print(f"{error=}")
            return ""

    # --------------------- whois details ----------------------
    # ["expiration_date", "registrar"]
    # not testing the following code since it's merely getting fields from the whois result
    @exception(LOGGER)
    def expiration_date(self) -> str:
        """
        Util for getting the expiration date for the searched domain

        :return: The string format for the expiration date
        :rtype: str
        """
        whois_result = self.search_whois()
        if whois_result:
            return str(whois_result["expiration_date"])
        return ""

    @exception(LOGGER)
    def registrar(self) -> str:
        """
        Util for getting the registrar for the searched domain

        :return: The DNS registrar
        :rtype: str
        """
        whois_result = self.search_whois()
        if whois_result:
            return whois_result["registrar"]
        return ""

    # ---------------------- Email Provider ------------------------
    @exception(LOGGER)
    def email_provider(self) -> str:
        mx_record = self.get_result("mx")
        if len(mx_record) != 0:
            # check if the smtp domain name is within the mx string
            for domain in EMAIL_TABLE:
                if domain in mx_record:
                    return EMAIL_TABLE[domain]

        return ""

    # ------------------------------------------- Comparison --------------------------------------------------
    # check 'oldfunshinymelody.neverssl.com' for None SSL
    @exception(LOGGER)
    def has_https(self) -> bool:
        """
        Util for checking whether the domain has https

        :return: True if https exists, otherwise False
        :rtype: bool
        """
        # check whether the input site is a www domain
        try:
            https_url = f'https://{self._domain_string}' if self.get_result(
                "www") == "" else f'https://{self.get_result("www")}'

            https_url = urlparse(https_url)
            connection = http.client.HTTPSConnection(https_url.netloc, timeout=2)
            connection.request('HEAD', https_url.path)
            return True if connection.getresponse() else False

        except http.client.HTTPException as error:
            LOGGER.exception(msg=f"HTTP client server Error: {error}")
            # print(f"{error=}")
            return False

        except BaseException as error:
            LOGGER.exception(msg=f"HTTP search Error: {error}")
            # print(f"{error=}")
            return False

        finally:  # always close the connection
            connection.close()

    @exception(LOGGER)
    def is_black_listed(self) -> bool:
        """
        Util for checking whether the domain is blacklisted by any providers

        :return: True if blacklisted, otherwise False
        :rtype: bool
        """
        return self._black_list_checker.is_black_listed(self._domain_string)

    #  ------------------- Output to dict ----------------------------------------
    @property
    def domain_info(self) -> dict:
        """
        Property domain_info is the fetched result for the given domain.

        :return: The dictionary result of the search result
        :rtype: dict
        """
        # Update check_time every search -> format: 2013-09-18 11:16:32
        self.check_time = str(datetime.datetime.now(pytz.timezone("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S"))
        start_time = time.perf_counter()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            check_time = self.check_time
            a_record = executor.submit(self.get_result, "a").result()
            aaaa_record = executor.submit(self.get_result, "aaaa").result()
            mx_record = executor.submit(self.get_result, "mx").result()
            soa_record = executor.submit(self.get_result, "soa").result()
            www_address = executor.submit(self.get_result, "www").result()
            name_server = executor.submit(self.get_result, "ns").result()
            txt_record = executor.submit(self.get_result, "txt").result()
            ipv4_list = executor.submit(self.get_result, "ipv4").result()
            ipv6_list = executor.submit(self.get_result, "ipv6").result()
            # properties can't multi-thread
            asn_record = executor.submit(self.asn).result()
            xfr_record = executor.submit(self.xfr).result()
            ptr_record = executor.submit(self.ptr).result()
            registrar = executor.submit(self.registrar).result()
            expiration_date = executor.submit(self.expiration_date).result()
            email_exchange_service = executor.submit(self.email_provider).result()
            # srv_record = executor.submit(self.srv).result()
            o365_record = executor.submit(self.o365_results).result()
            has_https = executor.submit(self.has_https).result()
            is_blacklisted = executor.submit(self.is_black_listed).result()

        domain_search_result = {
            "domain_name": self._domain_string,
            "check_time": check_time,
            "a": a_record,
            "aaaa": aaaa_record,
            "mx": mx_record,
            "soa": soa_record,
            "www": www_address,
            "ns": name_server,
            "txt": txt_record,
            "ipv4": ipv4_list,
            "ipv6": ipv6_list,
            "asn": asn_record,
            "xfr": xfr_record,
            "ptr": ptr_record,
            "registrar": registrar,
            "expiration_date": expiration_date,
            "email_exchange_service": email_exchange_service,
            "srv": None,  # srv_record,
            "o365": o365_record,
            "has_https": has_https,
            "is_blacklisted": is_blacklisted
        }
        end_time = time.perf_counter()
        search_used_time: str = f"{round(end_time - start_time, 2)} second(s)"
        domain_search_result["search_used_time"] = search_used_time

        return domain_search_result
