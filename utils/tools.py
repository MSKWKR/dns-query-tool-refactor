"""DNS Tool Box"""
import re
import dns.resolver
import dns.exception
import socket
from typing import Union, List


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
            answers = dns.resolver.resolve("www." + self._domain_string, "A")
            if answers:
                return answers
            else:
                return None

        except (dns.exception.FormError, dns.exception.SyntaxError, dns.exception.UnexpectedEnd,
                dns.exception.TooBig, dns.exception.Timeout, dns.resolver.NXDOMAIN
                , dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.YXDOMAIN,
                dns.name.EmptyLabel, socket.error):
            return None

    def search_cname(self, o365_record_type: str) -> str:
        record_type = o365_record_type.lower()
        match record_type:
            case "auto":
                search_string = f"autodiscover.{self._domain_string}"
                regex_comparison_pattern = r"autodiscover.outlook.com"
            case "msoid":
                search_string = f"msoid.{self._domain_string}"
                regex_comparison_pattern = r"clientconfig.microsoftonline-p.net"
            case "lync":
                search_string = f"lyncdiscover.{self._domain_string}"
                regex_comparison_pattern = r"webdir.online.lync.com",

        try:
            cname_answers = dns.resolver.resolve(search_string, "CNAME")
            for answer in cname_answers:
                if re.search(regex_comparison_pattern, str(answer)):
                    return "correct"
                else:
                    return "misconfigured"

        except Exception:
            return "misconfigured"

        # ------------------------- Fetch Result Tools ------------------------------------

    def get_result(self, record_type: str) -> Union[str, List]:
        """
        Function for getting the asked Record Type.
        Can accept input Record type 'A', 'AAAA', 'NS', 'MX', 'TXT', 'SOA', 'WWW' with its upper and lower cases.
        Return an empty string if input record type is incorrect or the domain itself malfunctioned.

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

            case "NS":
                answers = self.search(record_type)
                ns_result = []
                for answer in answers:
                    ns_result.append(str(answer))

                return answer

            case "TXT":
                answers = self.search(record_type)
                txt_result = []
                if not answers:
                    return txt_result
                for answer in answers:
                    txt_result.append(str(answer))
                return txt_result

            case "WWW":
                answers = self.search_www()
                return f"www.{self._domain_string}" if answers else ""

            case _:
                raise NameError(f"Record Type Input Error: {record_type}")

    def get_o365_result(self, o365_type: str):
        o365_type = o365_type.lower()
        match o365_type:
            case "auto":
                pass
            case "msoid":
                pass

            case "lync":
                pass

            case "365mx":
                pass

            case "spf":
                pass

            case "sipdir":
                pass

            case "sipfed":
                pass

            case _:
                pass


def main():
    toolbox = DNSToolBox()
    toolbox.set_domain_string("freedom.net.tw")
    # while True:
    #     test_site = input("Enter Domain Name: ")
    #     toolbox.set_domain_string(test_site)
    #     finished_record_type = ["a", "aaaa", "ns", "mx", "txt", "soa", "www"]
    #     for dns_record_type in finished_record_type:
    #         result = toolbox.get_result(dns_record_type)
    #         print(f"{dns_record_type}: {result}")
    #
    #     if input("Do you want to continue? (y/n)").lower() == "n":
    #         break
    for cname_type in ["auto", "msoid", "lync"]:
        print(toolbox.search_cname(cname_type))


if __name__ == "__main__":
    main()
