import pytest
from utils import tools


class TestDNSToolBox:
    TEST_DOMAIN = "example.com"
    TEST_TOOLBOX = tools.DNSToolBox()
    # is this the valid way?
    TEST_TOOLBOX.set_domain_string(TEST_DOMAIN)

    @pytest.mark.parametrize("test_input, expected",
                             [(TEST_DOMAIN, TEST_DOMAIN)])
    def test_set_domain_string(self, test_input, expected):
        # the set domain string equal to the given domain constant
        assert self.TEST_TOOLBOX.set_domain_string(test_input) == expected

    def test_A(self):

        want = "93.184.216.34"
        have = self.TEST_TOOLBOX.A
        assert want == have

    def test_AAAA(self):
        want = "2606:2800:220:1:248:1893:25c8:1946"
        have = self.TEST_TOOLBOX.AAAA
        assert want == have
