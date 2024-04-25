"""Tests for utility functions."""
from unittest import TestCase
from multidig.helpers import utils

class TestHelperUtils(TestCase):
    """Test reading of yaml config files."""

    def test_generate_client_cookie(self):
        """Check that a DNS client cookie gets computed."""
        cookie = utils.generate_client_cookie()
        self.assertIs(
            type(cookie),
            bytes,
            msg="Cookie is a bytes string."
        )

    def test_byte_compare(self):
        """Test that the byte compare function is working as expected."""
        string1 = utils.generate_client_cookie()
        string_same = string1
        string_different = utils.generate_client_cookie()
        self.assertTrue(
            utils.compare_byte_string_prefix(string1, string_same, 8),
            msg="Both strings match"
        )
        self.assertFalse(
            utils.compare_byte_string_prefix(string1, string_different, 8),
            msg="Strings don't match"
        )
