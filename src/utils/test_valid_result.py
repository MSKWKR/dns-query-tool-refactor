import pytest
from util_tools.constants_for_test import different_incorrect_a_records, different_incorrect_aaaa_records

from util_tools.valid_result import Validator

test_validator = Validator()


@pytest.mark.parametrize("input_", different_incorrect_a_records)
def test_is_invalid_a(input_: str):
    have = test_validator.is_valid("A", input_)
    # the test checks all the incorrect a record
    expected = False
    assert have == expected


@pytest.mark.parametrize("input_", different_incorrect_aaaa_records)
def test_is_invalid_aaaa(input_):
    have = test_validator.is_valid("AAAA", input_)
    expected = False
    assert have == expected
