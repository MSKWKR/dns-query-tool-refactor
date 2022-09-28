import pytest

from src.utils.blacklist_checker import BlackListChecker
from src.utils.constants_for_test import non_blacklisted_sites

test_black_list_checker = BlackListChecker()


@pytest.mark.parametrize("input_", non_blacklisted_sites)
def test_not_black_listed(input_):
    have = test_black_list_checker.is_black_listed(input_)
    expected = False

    assert have == expected
