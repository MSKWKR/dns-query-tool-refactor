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
                if search_result in ["0.0.0.0", "255.255.255.255", "127.0.0.1"]:
                    # reserved address
                    return False

                for char in search_result:
                    # shouldn't contain characters other than numeric numbers
                    if char.isalpha():
                        return False

                split_char_list = search_result.split(".")
                print(split_char_list)
                if len(split_char_list) != 4:
                    # shouldn't have less than 3 dots
                    return False

                if split_char_list[0] in ("0", "10"):
                    # IPv4 can't start with 0 or 10
                    return False

                for num in split_char_list:
                    # shouldn't have any numbers that is greater than 256

                    if int(num) >= 256:
                        return False
                    # shouldn't have any numbers that is greater than 256
                    elif int(num) < 0:
                        return False

                return True

            case "AAAA":
                pass

            case "MX":
                pass

            case "SOA":
                pass


if __name__ == "__main__":
    v = Validator()
    # for ip in different_incorrect_a_record:
    #     if not v.is_valid("A", ip):
    #         print(f"{ip} isn't valid\n")
    #     else:
    #         print(f"{ip} is valid\n")

    result = v.is_valid("A", "93.184.216.34")
    print(result)
