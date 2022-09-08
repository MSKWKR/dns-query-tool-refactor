"""DNS Tool Box"""
import dns.resolver
import dns.exception


class DNSToolBox:
    """
    DNSToolBox is a generic-style set that contains the method that needed to check the domain string
    """

    # the tool is defaulted with nothing
    def __init__(self):
        """Initializes class attribute"""
        self._domain_string = None

    def set_domain_string(self, domain_string: str) -> str:
        """Set_domain_string parses, initialize and return the pure domain string
        :param domain_string: str
        :return: str
        """

        self._domain_string = domain_string
        return domain_string

    def search_with_type(self, record_type: str) -> str:
        """
        The method search with type is a generic function that takes the given record type and search with dns resolver.

        Can accept input record type 'A', 'AAAA', 'NS', 'MX', 'TXT', 'SOA', 'WWW' with its upper and lower cases.
        Return an error string if input record type is incorrect or the domain itself malfunctioned.

        :param record_type: DNS record type
        :type record_type: str

        :return: The search result
        :rtype: str
        """
        # print(f"{record_type:}")
        # turn input all to uppercase for comparison
        record_type = record_type.upper()
        match record_type:
            case ("A" | "AAAA" | "NS" | "MX" | "TXT" | "SOA"):
                try:
                    # the answer is an iterator of type records, need to loop through in order to get the data
                    answers = dns.resolver.resolve(self._domain_string, record_type)
                    for answer in answers:
                        # answer is a dns.resolver.Answer instance, return type should be a converted string
                        return str(answer)

                # Error handling when input domain is incorrect
                except Exception as error:
                    match Exception:
                        # Handle expected error
                        case (dns.exception.FormError | dns.exception.SyntaxError | dns.exception.UnexpectedEnd,
                              dns.exception.TooBig | dns.exception.Timeout | dns.resolver.NXDOMAIN
                              | dns.resolver.NoAnswer | dns.resolver.NoNameservers):
                            return f"Domain Name Error: {error}"
                        # Handle unexpected error
                        case _:
                            return f"Unexpected Error: {error}"
            case "WWW":
                try:
                    answers = dns.resolver.resolve("www." + self._domain_string, "A")
                    if answers:
                        return f"www.{self._domain_string}"
                except Exception as error:
                    return f"www domain error: {error}"
            case _:
                raise NameError(f"Record Type Input Error: {record_type}")


def main():
    toolbox = DNSToolBox()
    # test_site = "example.com"
    while True:
        test_site = input("Enter Domain Name: ")
        toolbox.set_domain_string(test_site)
        search_type = input("Enter Records you want to check: ").upper()
        print("\n", toolbox.search_with_type(search_type), "\n")
        if input("Do you want to continue? (y/n)").lower() == "n":
            break


if __name__ == "__main__":
    main()
