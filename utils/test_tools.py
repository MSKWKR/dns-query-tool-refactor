import pytest

import tools

toolbox = tools.DNSToolBox


@pytest.mark.parametrize("input_, expected", [("test_address.", "test_address"), ("", "")])
def test_strip_last_dot(input_, expected):
    have = toolbox.strip_last_dot(input_)
    assert have == expected


raw_domain_check_data = [
    ("", None),
    ("ksjdhfskj", None),
    ("example.com", "example.com"),
    ("https://example.com", "example.com"),
    ("https://www.example.com", "example.com"),
    ("'https://www.e{xam}ple.com'", "example.com"),
    ("https://edward.example.com", "example.com"),
    ("https://example.com.hk", "example.com.hk"),
    ("ftp://example.com", "example.com"),
]


@pytest.mark.parametrize("input_, expected", raw_domain_check_data)
def test_parse_raw_domain(input_, expected):
    have = toolbox.parse_raw_domain(input_)
    assert have == expected
