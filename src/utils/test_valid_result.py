import pytest

from src.utils.constants_for_test import different_incorrect_a_records, different_incorrect_aaaa_records, \
    different_incorrect_mx_records, different_incorrect_soa_records, different_incorrect_srv_records
from src.utils.valid_result import Validator

test_validator = Validator("example.com")


@pytest.mark.parametrize("input_", different_incorrect_a_records)
def test_is_invalid_a(input_: str):
    have = test_validator.is_valid("A", input_)
    # the test checks all the incorrect a record
    expected = False
    assert have == expected


@pytest.mark.parametrize("input_", different_incorrect_aaaa_records)
def test_is_invalid_aaaa(input_: str):
    have = test_validator.is_valid("AAAA", input_)
    expected = False
    assert have == expected


@pytest.mark.parametrize("input_", different_incorrect_mx_records)
def test_invalid_mx(input_: str):
    have = test_validator.is_valid("MX", input_)
    expected = False

    assert have == expected


@pytest.mark.parametrize("input_", different_incorrect_soa_records)
def test_invalid_soa(input_: str):
    have = test_validator.is_valid("SOA", input_)
    expected = False

    assert have == expected


@pytest.mark.parametrize("input_", different_incorrect_srv_records)
def test_is_invalid_srv(input_):
    have = test_validator.is_valid_srv(input_)
    expected = False

    assert have == expected
