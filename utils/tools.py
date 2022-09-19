"""DNS Tool Box"""
import datetime
import http.client
import re
import socket
from typing import List
from urllib.parse import urlparse

import dns.exception
import dns.resolver
import dns.zone
import pytz as pytz
import whois
from ipwhois.asn import IPASN
from ipwhois.net import Net

import blacklist_checker
from constants import EMAIL_TABLE, SRV_LIST, YELLOW_TITLE, BLANK_CUT

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
        self.check_time = datetime.datetime.now(pytz.timezone("Asia/Taipei"))

        self._domain_string = None
        self._res = dns.resolver.Resolver()
        self._black_list_checker = blacklist_checker.BlackListChecker()

    def __repr__(self):
        return f"DNSToolBox{self._domain_string}"

    # ------------------------- Helper Function ------------------------------------

    @classmethod
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
    def parse_raw_domain(cls, input_domain: str) -> str | None:
        """
        Method parse_raw_domain cleanses the input domain and return the domain name

        :param input_domain: Raw input domain, might have error key-in symbols
        :type: str

        :return: The cleansed domain string
        :rtype: str
        """

        pattern = '[^A-Za-z0-9.:/]'
        input_domain = urlparse(re.sub(pattern=pattern, repl="", string=input_domain))
        # doesn't strip the www
        input_domain = input_domain.netloc or input_domain.path
        if input_domain == "":
            return None
        input_domain = re.sub(r'(www.)(?!com)', r'', input_domain)
        return input_domain

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
    def search(self, record_type: str) -> dns.resolver.Resolver | None:
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
            print(f"{error=}")
            return None

    def search_www(self) -> dns.resolver.Resolver | None:
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
            print(f"{error=}")

        return None

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
            print(f"{error=}")
            return None

    @classmethod
    def search_ipwhois_asn(cls, ip_address: str) -> dict[any]:
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
            print(f"{error=}")
            return asn_results

    def search_o365(self, record_type: str) -> dns.resolver.Resolver | None:
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
            print(f"{error=}")

        return answers

    def get_srv_results(self, proto="tcp") -> List[str]:
        """
            Util function for searching srv records for with the given protocol name, default to tcp.

            :return: The searched srv records
            :rtype: List[str]
        """
        proto = proto.lower()
        srv_result_list = []
        for n in range(len(SRV_LIST)):
            try:
                srv_record = dns.resolver.resolve(f"_{SRV_LIST[n]}._{proto}.{self._domain_string}", "SRV")
                for data in srv_record:
                    srv_result_list.append(data.to_text())

            except ToolBoxErrors as error:
                # print(f"{error=}")
                pass
        return srv_result_list

    # ------------------------- Get Result Tools ------------------------------------

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
                if answers:
                    # answers is an iterator of type records, need to loop through in order to get the data
                    for answer in answers:
                        # answer is a dns.resolver.Answer instance, return type should be a converted string
                        return str(answer)
                else:
                    return ""

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
                            ip_list.append(str(a_data))
                    except ToolBoxErrors as error:
                        print(f"{error=}")
                return ip_list

            case "WWW":
                answers = self.search_www()
                return f"www.{self._domain_string}" if answers else ""

            case _:
                raise NameError(f"Record Type Input Error: {record_type}")

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

    # ---------------------------------------------- ToolBox Properties -----------------------------------------
    @property
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
    @property
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

    @property
    def srv(self) -> dict[str: List[str]]:
        """
        Util for getting the srv record for the searched domain

        :return: The dictionary for the SRV records with field udp, tcp and tls
        :rtype: dict
        """

        srv_result_dict = {
            "UDP": self.get_srv_results("udp"),
            "TCP": self.get_srv_results("tcp"),
            "TLS": self.get_srv_results("tls")
        }

        return srv_result_dict

    @property
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
            print(f"{error=}")

        return xfr_list

    @property
    def ptr(self) -> str:
        """
        Util function for getting the ptr record using reverse query

        :return: The PTR record
        """
        try:
            address = dns.reversename.from_address(self.get_result("a"))
            return dns.resolver.resolve(str(address), "PTR")[0]
        except ToolBoxErrors as error:
            print(f"{error=}")
            return ""

    # --------------------- whois details ----------------------
    # ["expiration_date", "registrar"]
    # not testing the following code since it's merely getting fields from the whois result
    @property
    def expiration_date(self) -> str:
        """
        Util for getting the expiration date for the searched domain

        :return: The string format for the expiration date
        :rtype: str
        """
        whois_result = self.search_whois()
        if whois_result:
            return whois_result["expiration_date"]
        return ""

    @property
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
    @property
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
            print(f"{error=}")
            return False

        except BaseException as error:
            print(f"{error=}")
            return False

        finally:  # always close the connection
            connection.close()

    def is_black_listed(self) -> bool:
        """
        Util for checking whether the domain is blacklisted by any providers

        :return: True if blacklisted, otherwise False
        :rtype: bool
        """
        return self._black_list_checker.is_black_listed(self._domain_string)

    def ns_nested_in_ip(self) -> bool:
        ns_list = self.get_result("ns")
        ipv4_list = self.get_result("ipv4")


def _main():
    toolbox = DNSToolBox()
    continue_ = True
    while continue_:
        test_site = input("Enter Domain Name: ")

        toolbox.set_domain_string(test_site)
        finished_record_type = ["a", "aaaa", "mx", "soa", "www", "ns", "txt", "ipv4", "ipv6"]
        for dns_record_type in finished_record_type:
            result = toolbox.get_result(dns_record_type)
            print(f"{YELLOW_TITLE}{dns_record_type}:{BLANK_CUT} {result}\n")

        print(f"{YELLOW_TITLE}asn:{BLANK_CUT} {toolbox.asn}\n")
        print(f"{YELLOW_TITLE}xfr:{BLANK_CUT} {toolbox.xfr}\n")
        print(f"{YELLOW_TITLE}ptr:{BLANK_CUT} {toolbox.ptr}\n")
        print(f"{YELLOW_TITLE}registrar:{BLANK_CUT} {toolbox.registrar}\n")
        print(f"{YELLOW_TITLE}expiration date:{BLANK_CUT} {toolbox.expiration_date}\n")
        print(f"{YELLOW_TITLE}email_exchange_service:{BLANK_CUT} {toolbox.email_provider}\n")
        # print(f"{YELLOW_TITLE}srv:{BLANK_CUT} {toolbox.srv}\n")

        print(f"{YELLOW_TITLE}o365:{BLANK_CUT} {toolbox.o365_results}\n")

        print(f"{YELLOW_TITLE}has_https:{BLANK_CUT} {toolbox.has_https()}\n")
        print(f"{YELLOW_TITLE}is_blacklisted:{BLANK_CUT} {toolbox.is_black_listed()}\n")
        print(f"{YELLOW_TITLE}check_time:{BLANK_CUT} {toolbox.check_time}")
        if input("Do you want to continue? (y/n)").lower() == "n":
            continue_ = False


if __name__ == "__main__":
    _main()
