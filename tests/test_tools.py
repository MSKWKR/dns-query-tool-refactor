import pytest

from src.utils.constants_for_test import raw_domain_check_data, correct_string_results, correct_list_results, \
    correct_asn, correct_srv
from src.utils.tools import DNSToolBox

# @pytest.fixture
# def newToolBox():
#     toolbox = DNSToolBox()
#     return toolbox

newToolBox = DNSToolBox()


# ------------------- code interworking -----------------------------
@pytest.mark.parametrize("input_, expected", [("test_address.", "test_address"), ("", "")])
def test_strip_last_dot(input_, expected):
    have = newToolBox.strip_last_dot(input_)
    assert have == expected


@pytest.mark.parametrize("input_, expected", raw_domain_check_data)
def test_parse_raw_domain(input_, expected):
    have = newToolBox.parse_raw_domain(input_)
    assert have == expected


@pytest.mark.parametrize("domain, input_, expected", correct_string_results)
def test_get_result_correct_string(domain, input_, expected):
    newToolBox.set_domain_string(domain)
    have = newToolBox.get_result(input_)
    assert have == expected


@pytest.mark.parametrize("domain, input_, expected", correct_list_results)
def test_get_result_correct_list(domain, input_, expected):
    newToolBox.set_domain_string(domain)
    have = set(newToolBox.get_result(input_))
    assert have == expected


@pytest.mark.parametrize("domain", ["example.com"])
def test_has_https(domain):
    newToolBox.set_domain_string(domain)
    have = newToolBox.has_https()
    expect = True
    assert have == expect


@pytest.mark.parametrize("domain, expected", correct_asn)
def test_asn(domain, expected):
    newToolBox.set_domain_string(domain)
    have = newToolBox.asn()
    for asn_record in have:
        assert set(have[asn_record]) == expected[asn_record]


@pytest.mark.parametrize("domain, expected", correct_srv)
def test_srv(domain, expected):
    newToolBox.set_domain_string(domain)
    have = newToolBox.srv()
    expect = expected
    assert have == expect