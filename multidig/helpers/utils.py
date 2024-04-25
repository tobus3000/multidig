"""
Collection of helper functions to be used all over the program.

Functions:
    get_yml_config
"""
import random
import re

def generate_client_cookie() -> bytes:
    """
    Generate a random 32-bit unsigned integer as the client cookie.
    The client cookie should be unique for each DNS session to prevent
    certain types of attacks.

    :return: The generated client cookie.
    :rtype: bytes
    """
    random_number = random.randint(0, 2**32 - 1)
    return random_number.to_bytes(length=8, byteorder='little')

def compare_byte_string_prefix(
        byte_string1: bytes,
        byte_string2: bytes,
        prefix_length: int
    ) -> bool:
    """
    Compare the first part of two byte strings up to a specified prefix length.

    :param byte_string1: The first byte string.
    :type byte_string1: bytes
    :param byte_string2: The second byte string.
    :type byte_string2: bytes
    :param prefix_length: The length of the prefix to compare.
    :type prefix_length: int
    :return: True if the specified prefixes are equal, False otherwise.
    :rtype: bool
    """
    prefix1 = byte_string1[:prefix_length]
    prefix2 = byte_string2[:prefix_length]
    return prefix1 == prefix2

def is_valid_hostname(hostname):
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    if len(hostname) > 253:
        return False

    labels = hostname.split(".")

    # the TLD must be not all-numeric
    if re.match(r"[0-9]+$", labels[-1]):
        return False

    allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(label) for label in labels)

def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))
