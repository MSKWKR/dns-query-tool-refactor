import dns
import pytest
from utils import tools


class TestDNSToolBox:
    TEST_DOMAIN = "example.com"
    TEST_TOOLBOX = tools.DNSToolBox()
    # is this the valid way?
    TEST_TOOLBOX.set_domain_string(TEST_DOMAIN)

    @pytest.mark.parametrize("test_input, expected", [
        pytest.param(TEST_DOMAIN, TEST_DOMAIN),
        pytest.param("", ""),
        pytest.param("not a domain", "not a domain")
    ])
    def test_set_domain_string(self, test_input, expected):
        # the set domain string equal to the given domain constant
        assert self.TEST_TOOLBOX.set_domain_string(test_input) == expected

    # ----------------------- domain string test -------------------------------

    @pytest.mark.xfail(raises=dns.resolver.NoNameservers)
    def test_get_result_empty_domain(self):
        # test empty input
        self.TEST_TOOLBOX.set_domain_string("")
        self.TEST_TOOLBOX.get_result("A")

    # should xpass since it should raise and error
    @pytest.mark.xfail(raises=dns.resolver.NoNameservers)
    # not sure if the error raised here is correct?
    def test_get_result_wrong_domain_string(self):
        # test wrong input
        self.TEST_TOOLBOX.set_domain_string("sdfasdfsdfsdf")
        self.TEST_TOOLBOX.get_result("A")

    # ----------------------- different input type test ------------------------------
    @pytest.mark.parametrize("test_input, expected", [
        pytest.param("a", "93.184.216.34"),
        pytest.param("aaaa", "2606:2800:220:1:248:1893:25c8:1946"),
        pytest.param("www", "www.example.com"),
        pytest.param("mx", "0 ."),
        pytest.param("soa", "ns.icann.org. noc.dns.icann.org. 2022090401 7200 3600 1209600 3600")
    ])
    def test_get_result(self, test_input, expected):
        self.TEST_TOOLBOX.set_domain_string(self.TEST_DOMAIN)
        assert self.TEST_TOOLBOX.get_result(test_input) == expected
