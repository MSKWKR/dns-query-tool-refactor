import ipaddress
import re
from typing import List

from .constants import SPECIAL_ADDRESS_BLOCKS


class Validator:

    @classmethod
    def is_valid(cls, url: str, record_type: str, search_result: any) -> bool:
        """
        Function that checks whether the given search_result with the matched record type is valid.

        :param url:
        :param record_type: The DNS record type to check
        :type: str

        :param search_result: The DNS result fetched by the API
        :type: any

        :return: True if the result is valid, else False
        :rtype: bool
        """
        match record_type:
            case "A":
                # shouldn't contain any character that isn't 0-9
                regex_pattern = r'^[0-9.]'
                if not re.search(pattern=regex_pattern, string=search_result):
                    return False

                split_char_list: List[str] = search_result.split(".")
                if len(split_char_list) != 4:
                    # shouldn't have less than 3 dots
                    return False

                for num in split_char_list:
                    # shouldn't have any numbers that is greater than 256
                    if int(num) >= 256:
                        return False
                    # shouldn't have any numbers that is greater than 256
                    elif int(num) < 0:
                        return False

                future_reserved_range = [str(num) for num in range(240, 256)]  # 240 - 255
                multicast_reserved_range = [str(num) for num in range(224, 240)]  # 224 - 239

                if split_char_list[0] in ("0", "10", "127", *future_reserved_range, *multicast_reserved_range):
                    # 0, current software network
                    # 10, local communications within private network
                    # 127, loopback addresses
                    # 240.0.0.0- 255.255.255.254 is reserved for future use
                    # 255.255.255.255 is reserved for limited broadcast
                    # 224.0.0.0 - 239.255.255.255 is used for IP multicast
                    return False

                elif (split_char_list[0], split_char_list[1]) in [("169", "254"), ("192", "168")]:
                    # 168.254.0.0 - 169.254.255.255 is used for link-local addresses
                    # 192.168.0.0 - 192.168.255.255 is used for private local communications
                    return False

                elif (split_char_list[0], split_char_list[1], split_char_list[2]) in [
                    ("198", "51", "100"), ("192", "88", "99"), ("192", "0", "0"),
                    ("192", "0", "2"), ("203", "0", "113"), ("233", "252", "0")
                ]:
                    # 192.88.99.0 - 192.88.99.255 is reserved for IPv6 to IPv4 relay
                    # 192.0.0.0 - 192.0.0.255 is reserved for IETF protocol assignments
                    # 192.0.2.0 - 192.0.2.255 is assigned for TEST-NET-1
                    # 198.51.100.0 - 198.51.100.255 is assigned for TEST-NET-2
                    # 203.0.113.0 - 203.0.113.255 is assigned for TEST-NET-3
                    return False

                for address_block in SPECIAL_ADDRESS_BLOCKS:
                    if search_result in SPECIAL_ADDRESS_BLOCKS[address_block]:
                        return False

                return True

            case "AAAA":
                # shouldn't contain any character that isn't 0-9, A-F(a-f)
                regex_pattern = r'^[0-9a-fA-F:.]'
                if not re.search(pattern=regex_pattern, string=search_result):
                    return False
                elif search_result == "::":

                    return False

                search_result = ipaddress.IPv6Address(search_result)
                if search_result.is_loopback or search_result.is_multicast or search_result.is_private \
                        or search_result.is_reserved or search_result.is_link_local or search_result.is_site_local:
                    return False
                return True

            case "MX":
                if len(search_result) >= 256:
                    return False
                return True

            case "SRV":
                # might have empty results
                if search_result == "":
                    return True
                # soa and srv record should at least contain domain
                elif url not in search_result:
                    return False

                return True

            case _:
                return True
