import random

import pytest

from constants_for_test import raw_domain_check_data, correct_string_results, correct_list_results, \
    different_incorrect_a_record
from tools import DNSToolBox

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


# ----------------- Mock and try to break the code -------------------------------


class MockToolBox(DNSToolBox):
    def get_result(self, record_type: str) -> str:
        record_type = record_type.upper()
        match record_type:
            case "A":
                result = random.choice(different_incorrect_a_record)
                if result in ["0.0.0.0", "255.255.255.255", "127.0.0.1"]:
                    raise TypeError("Incorrect form Record A, reserved IPv4 address")
                return result


def test_get_result_a():
    m = MockToolBox()
    assert m.get_result("a") == "0.0.0.0"
