class Validator:
    def __init__(self):
        pass

    @staticmethod
    def is_valid(record_type: str, result: any) -> bool:
        match record_type:
            case "A":
                if result in ["0.0.0.0", "255.255.255.255", "127.0.0.1"]:
                    raise ValueError("Incorrect form Record A, reserved IPv4 address")

            case "AAAA":
                pass

            case "MX":
                pass

            case "SOA":
                pass



