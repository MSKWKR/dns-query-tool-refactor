import whois

import dns.resolver


# DNSToolBox is a generic-style set that contains the method that needed to check the domain string
class DNSToolBox:
    # the tool is defaulted with nothing
    def __init__(self):
        # set implicit domain string
        self._domain_string = None

    # initialize the tool domain string to the given string
    def set_domain_string(self, domain_string: str):
        self._domain_string = domain_string

    # check factor A for IPv4
    @property
    def A(self) -> str:
        # the answer is an iterator of 'A' records, need to loop through in order to get the data
        answers = dns.resolver.resolve(self._domain_string, "A")
        for rdata in answers:
            print("Host", rdata.exchange, "has preference", rdata.preference)

    # check factor AAAA for IPv6
    @property
    def AAAA(self) -> str:
        return "aaaa"

    # check factor NS
    @property
    def NS(self):
        return "NS"

    # check factor MX
    @property
    def MX(self):
        answers = dns.resolver.resolve(self._domain_string, "MX")
        for rdata in answers:
            print("Host", rdata.exchange, "has preference", rdata.preference)

    # check whether the given site has a www domain
    @property
    def have_www(self) -> bool:
        return True


def main():
    toolbox = DNSToolBox()
    test_site = "freedom.net.tw"
    toolbox.set_domain_string(test_site)
    print(toolbox.MX)


if __name__ == "__main__":
    main()
