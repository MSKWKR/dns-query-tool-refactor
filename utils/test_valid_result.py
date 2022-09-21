import pytest

from constants_for_test import different_incorrect_a_record
from valid_result import Validator

test_validator = Validator()


@pytest.mark.parametrize("input_", different_incorrect_a_record)
def test_is_invalid_a(input_: str):
    have = test_validator.is_valid("A", input_)
    # the test checks all the incorrect a record
    expected = False
    assert have == expected
