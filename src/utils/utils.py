import ipaddress
from typing import List


def get_ipv4_range(start_ip: str, end_ip: str) -> List[str]:
    """
    Util function for getting all IPv4 addresses within the given range
    :param start_ip: The starting IPv4 address
    :param end_ip: The ending IPv4 address
    :type: str

    :raises ValueError: If the input ending IP is before the starting IP

    :return: A List of IPv4 addresses within the given range
    :rtype: List[str]
    """
    ipv4_range_list: List[str] = []
    try:
        start_ip = int(ipaddress.IPv4Address(start_ip))
        end_ip = int(ipaddress.IPv4Address(end_ip))
        if start_ip > end_ip:
            raise ValueError(
                f"End IP: {ipaddress.IPv4Address(end_ip)} shouldn't be smaller than start IP: {ipaddress.IPv4Address(start_ip)}")
        for ip_int in range(start_ip, end_ip + 1):
            ipv4_range_list.append(str(ipaddress.IPv4Address(ip_int)))

    except ipaddress.AddressValueError as error:
        print(f"{error=}")

    return ipv4_range_list
