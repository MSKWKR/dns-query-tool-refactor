import pytest

from blacklist_checker import BlackListChecker
from constants_for_test import blacklisted_sites

test_black_list_checker = BlackListChecker()


@pytest.mark.parametrize("input_", blacklisted_sites)
def test_is_black_listed(input_):
    have = test_black_list_checker.is_black_listed(input_)
    expected = True

    assert have == expected
