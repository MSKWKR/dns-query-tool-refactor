"""DNS Tool Box"""
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

    def set_domain_string(self, domain_string: str) -> str:
        """Set_domain_string parses, initialize and return the pure domain string
        :param domain_string: The original input string(unparsed)
        :type: str

        :return: The parsed, usable domain
        :rtype: str
        """

        self._domain_string = domain_string
        return domain_string

    def search(self, record_type: str) -> Union[dns.resolver.Resolver, None]:
        """
        The method search with type is a generic function
        wraps search of the given record type and teh exceptions.
        :param record_type:
        :return:
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
        :return:
        """
        try:
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
            case ("A" | "AAAA" | "MX" | "SOA" | "CNAME"):
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


def main():
    toolbox = DNSToolBox()
    # test_site = "example.com"
    while True:
        test_site = input("Enter Domain Name: ")
        toolbox.set_domain_string(test_site)
        finished_record_type = ["a", "aaaa", "ns", "mx", "txt", "soa", "www", "cname"]
        for dns_record_type in finished_record_type:
            result = toolbox.get_result(dns_record_type)
            print(f"{dns_record_type}: {result}")

        if input("Do you want to continue? (y/n)").lower() == "n":
            break


if __name__ == "__main__":
    main()
