"""
Utility functions
"""

from base64 import b64encode
from socket import inet_aton, inet_ntoa
from struct import unpack, pack


def ip2long(ip_addr):
    """
    Convert IPv4 address in dotted notation to int

    :param str ip_addr: IPv4 address in dotted notation
    :return: IPv4 address as int
    :rtype: int
    """
    return unpack("!L", inet_aton(ip_addr))[0]


def long2ip(ip_long):
    """
    Convert IPv4 address as int to dotted notation

    :param int ip_long: IPv4 address as int
    :return: IPv4 address in dotted notation
    :rtype: str
    """
    return inet_ntoa(pack("!L", ip_long))


def base64_encode(file_path):
    """
    Encode a file contents to base64

    :param str file_path: Path to file
    :return: Base64 encoded string
    :rtype: str
    :raises: :py:exc:`OSError` if file not found or unreadable
    """
    with open(file_path, 'rb') as file_handle:
        file_content = file_handle.read()

    if not file_content:
        raise RuntimeError('Unable to read from file "{}"'.format(file_path))

    file_as_string = b64encode(file_content).decode('utf-8')
    # if base64 encoding fails:
    #   raise RuntimeError('Cannot convert file "{}" to base64 string'.format(file_path))

    return file_as_string
