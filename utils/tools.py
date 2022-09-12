"""DNS Tool Box"""
import re
from pprint import pprint
import dns.resolver
import dns.exception
import socket
from typing import Union, List
import whois
from ipwhois.net import Net
from ipwhois.asn import IPASN


class DNSToolBox:
    """
    DNSToolBox is a generic-style set that contains the method that needed to check the domain string
    """

    # the tool is defaulted with nothing
    def __init__(self):
        """Initializes class attribute"""
        self._domain_string = None
        self._res = dns.resolver.Resolver()

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
    def parse_raw_domain(cls, input_domain: str) -> str:
        """
        Method parse_raw_domain cleans the input domain and return the domain name
        :param input_domain: Raw input domain, might have error key-in symbols
        :type: str

        :return: The cleansed domain string
        :rtype: str
        """
        pattern = '[^A-Za-z0-9.]'
        input_domain = re.sub(pattern=pattern, repl="", string=input_domain)

        return input_domain

    def set_domain_string(self, domain_string: str) -> str:
        """Set_domain_string parses, initialize and return the pure domain string
        :param domain_string: The original input string(unparsed)
        :type: str

        :return: The parsed, usable domain
        :rtype: str
        """

        self._domain_string = DNSToolBox.parse_raw_domain(domain_string)
        return self._domain_string

    # def domain_status(self) -> str:
    #     """
    #     Function domain_status retrieve status code
    #     :return: Status String
    #     :rtype str
    #     """
    #     if not self.search_www():
    #         status_code = requests.get(f"https://{self._domain_string}").status_code
    #     else:
    #         domain_string = self.get_result("www")
    #         status_code = requests.get(f"https://{domain_string}").status_code
    #
    #     return str(status_code)

    # ------------------------- Search Tools ------------------------------------
    def search(self, record_type: str) -> Union[dns.resolver.Resolver, None]:
        """
        The method search with type is a generic function
        wraps search of the given record type and teh exceptions.
        :param record_type: The specific type we want to search for the domain
        :type: str

        :return: The answers by searching the given url with A Record type, None if not found
        :rtype dns.resolver.Resolver or None
        """
        try:
            return self._res.resolve(self._domain_string, record_type)
        # Return None when input domain is incorrect
        except (dns.exception.FormError, dns.exception.SyntaxError, dns.exception.UnexpectedEnd,
                dns.exception.TooBig, dns.exception.Timeout, dns.resolver.NXDOMAIN
                , dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.YXDOMAIN,
                dns.name.EmptyLabel, socket.error):
            return None

    def search_www(self) -> Union[dns.resolver.Resolver, None]:
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
            else:
                return None

        except (dns.exception.FormError, dns.exception.SyntaxError, dns.exception.UnexpectedEnd,
                dns.exception.TooBig, dns.exception.Timeout, dns.resolver.NXDOMAIN
                , dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.YXDOMAIN,
                dns.name.EmptyLabel, socket.error):
            return None

    def search_whois(self) -> Union[whois.parser.WhoisTw, None]:
        """
        Query a WHOIS server directly and return the parsed whois data.
        :return: The result for parsing the WHOIS data, None if not found
        :rtype whois.parser.WhoisTw, None
        """
        try:
            whois_result = whois.whois(self._domain_string)
            return whois_result
        except TypeError as error:
            print(f"{error=}")
            return None

    @classmethod
    def search_ipwhois_asn(cls, ip_address: str) -> dict:
        """
        Util function that searches the ASN records with the given IP
        :param ip_address: An IPv4 or IPv6 string
        :type: str

        :return: An ASN dictionary after parsing with the given ip address, returns an empty dictionary if not found
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

        except ValueError as error:
            print(f"{error=}")
            return asn_results

    # ------------------------- Fetch Result Tools ------------------------------------

    def get_result(self, record_type: str) -> Union[str, List]:
        """
        Function for getting the asked Record Type.
        Can accept input Record type 'A', 'AAAA', 'NS', 'MX', 'TXT', 'SOA', 'WWW' with its upper and lower cases.
        Return an empty string or empty list if input record type is incorrect or the domain itself malfunctioned.

        :param record_type: DNS record type
        :type record_type: str

        :return: The transformed search result
        :rtype: str, List
        """
        # print(f"{record_type:}")
        # turn input all to uppercase for comparison
        record_type = record_type.upper()
        match record_type:
            case ("A" | "AAAA" | "MX" | "SOA"):
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
                    a = dns.resolver.resolve(name, a_request_type)
                    for a_data in a:
                        ip_list.append(str(a_data))

                return ip_list

            case "WWW":
                answers = self.search_www()
                return f"www.{self._domain_string}" if answers else ""

            case _:
                raise NameError(f"Record Type Input Error: {record_type}")

    # Since the tool wants the specific field for the ASN,
    # this is dirty code that I didn't change much
    def get_asn_result(self) -> dict:
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

    # --------------------- whois details ----------------------
    # ["expiration_date", "registrar"]
    # not testing the following code since it's merely getting fields from the whois result
    def get_expiration_date(self) -> str:
        """
        Util for getting the expiration date for the searched domain
        :return: The string format for the expiration date
        :rtype: str
        """
        whois_result = self.search_whois()
        return whois_result["expiration_date"]

    def get_registrar(self) -> str:
        """
        Util for getting the registrar for the searched domain
        :return: The DNS registrar
        :rtype: str
        """
        whois_result = self.search_whois()
        return whois_result["registrar"]


def main():
    toolbox = DNSToolBox()
    while True:
        test_site = input("Enter Domain Name: ")
        toolbox.set_domain_string(test_site)
        finished_record_type = ["a", "aaaa", "mx", "soa", "www", "ns", "txt", "ipv4"]  # , "ipv6"]
        for dns_record_type in finished_record_type:
            result = toolbox.get_result(dns_record_type)
            print(f"{dns_record_type}: {result}\n")

        print(f"registrar: {toolbox.get_registrar()}\n")
        print(f"expiration date: {toolbox.get_expiration_date()}\n")

        pprint(f"asn: {toolbox.get_asn_result()}")
        if input("Do you want to continue? (y/n)").lower() == "n":
            break


if __name__ == "__main__":
    main()
