"""DNS Tool Box"""
import dns.resolver
import dns.exception


# DNS_EXCEPTIONS = (dns.exception.FormError, dns.exception.SyntaxError, dns.exception.UnexpectedEnd,
#                       dns.exception.TooBig, dns.exception.Timeout, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
#                       dns.resolver.NoNameservers)


# DNSToolBox is a generic-style set that contains the method that needed to check the domain string
class DNSToolBox:
    # the tool is defaulted with nothing
    def __init__(self):
        # set implicit domain string
        self._domain_string = None

    # initialize and return domain string to the class instance
    def set_domain_string(self, domain_string: str) -> str:
        self._domain_string = domain_string
        return domain_string

    # check factor A for IPv4
    @property
    def A(self) -> str:
        try:
            # the answer is an iterator of 'A' records, need to loop through in order to get the data
            answers = dns.resolver.resolve(self._domain_string, "A")
            for answer in answers:
                # answer is a dns.resolver.Answer instance, return type should be a converted string
                return str(answer)

        # Error handling when input domain is incorrect
        except Exception as error:
            match Exception:
                # Handle expected error
                case (dns.exception.FormError, dns.exception.SyntaxError, dns.exception.UnexpectedEnd,
                      dns.exception.TooBig, dns.exception.Timeout, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
                      dns.resolver.NoNameservers):
                    return f"Domain Name Error as: {error}"
                # Handle unexpected error
                case _:
                    return f"Unexpected Error as: {error}"

    # check factor AAAA for IPv6
    @property
    def AAAA(self) -> str:
        answers = dns.resolver.resolve(self._domain_string, "AAAA")
        for answer in answers:
            # answer is a DNS object, return a converted string
            return str(answer)

    # check factor NS
    # @property
    # def NS(self):
    #     return "NS"

    # check factor MX
    # @property
    # def MX(self):
    #     answers = dns.resolver.resolve(self._domain_string, "MX")
    #     for rdata in answers:
    #         print("Host", rdata.exchange, "has preference", rdata.preference)

    # check whether the given site has a www domain
    # @property
    # def have_www(self) -> bool:
    #     return True


def main():
    toolbox = DNSToolBox()
    # test_site = "example.com"
    while True:
        test_site = input("Enter Domain Name: ")
        toolbox.set_domain_string(test_site)
        print("\n", toolbox.A, "\n")
        if input("Do you want to continue? (y/n)").lower() == "n":
            break


if __name__ == "__main__":
    main()
