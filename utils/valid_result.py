from typing import List

from constants import SPECIAL_ADDRESS_BLOCKS


class Validator:
    def __init__(self):
        pass

    @staticmethod
    def is_valid(record_type: str, search_result: any) -> bool:
        """
        Function that checks whether the given search_result with the matched record type is valid.

        :param record_type: The DNS record type to check
        :type: str

        :param search_result: The DNS result fetched by the API
        :type: any

        :return: True if the result is valid, else False
        :rtype: bool
        """
        match record_type:
            case "A":
                for char in search_result:
                    # shouldn't contain characters other than numeric numbers
                    if char.isalpha():
                        return False

                split_char_list: List[str] = search_result.split(".")
                print(split_char_list)
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

                if split_char_list[0] in ("0", "10", "127"):
                    # 0, current software network
                    # 10, local communications within private network
                    # 127, loopback addresses
                    return False

                elif split_char_list[0] in (str(num) for num in range(240, 256)):
                    # 240.0.0.0- 255.255.255.254 is reserved for future use
                    # 255.255.255.255 is reserved for limited broadcast
                    return False

                elif split_char_list[0] in (str(num) for num in range(224, 240)):
                    # 224.0.0.0 - 239.255.255.255 is used for IP multicast
                    return False

                elif split_char_list[0] == "169" and split_char_list[1] == "254":
                    # 168.254.0.0 - 169.254.255.255 is used for link-local addresses
                    return False

                elif split_char_list[0] == "192" and split_char_list[1] == "168":
                    # 168.254.0.0 - 169.254.255.255 is used for link-local addresses
                    return False

                elif split_char_list[0] == "198" and split_char_list[1] == "51" and split_char_list[2] == "100":
                    # 198.51.100.0 - 198.51.100.255 is assigned for TEST-NET-2
                    return False

                elif split_char_list[0] == "192" and split_char_list[1] == "88" and split_char_list[2] == "99":
                    # 192.88.99.0 - 192.88.99.255 is reserved for IPv6 to IPv4 relay
                    return False

                elif split_char_list[0] == "192" and split_char_list[1] == "0" and split_char_list[2] == "0":
                    # 192.0.0.0 - 192.0.0.255 is reserved for IETF protocol assignments
                    return False

                elif split_char_list[0] == "192" and split_char_list[1] == "0" and split_char_list[2] == "2":
                    # 192.0.2.0 - 192.0.2.255 is assigned for TEST-NET-1
                    return False

                elif split_char_list[0] == "203" and split_char_list[1] == "0" and split_char_list[2] == "113":
                    # 203.0.113.0 - 203.0.113.255 is assigned for TEST-NET-3
                    return False

                elif split_char_list[0] == "233" and split_char_list[1] == "252" and split_char_list[2] == "0":
                    # 203.0.113.0 - 203.0.113.255 is assigned as MCAST-TEST-NET
                    return False

                for address_block in SPECIAL_ADDRESS_BLOCKS:
                    if search_result in SPECIAL_ADDRESS_BLOCKS[address_block]:
                        return False

                return True

            case "AAAA":
                pass

            case "MX":
                pass

            case "SOA":
                pass


def _main():
    v = Validator()
    print(v.is_valid("A", "0.0.0.0"))


if __name__ == "__main__":
    _main()
