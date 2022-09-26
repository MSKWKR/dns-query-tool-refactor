from pprint import pprint

from src.model.models import DNSRecord
from src.utils.tools import DNSToolBox


def main():
    toolbox = DNSToolBox()
    continue_ = True
    #
    # sqlite_file_name = "database.db"
    # sqlite_url = f"sqlite:///{sqlite_file_name}"
    # domain_database_engine = database.instantiate_engine(sqlite_url)

    while continue_:
        test_site = input("Enter Domain Name: ")
        toolbox.set_domain_string(test_site)
        domain_search_result = toolbox.domain_info
        pprint(domain_search_result)

        record = DNSRecord(
            check_time=domain_search_result["check_time"],
            a=domain_search_result["a"],
            aaaa=domain_search_result["aaaa"],
            mx=domain_search_result["mx"],
            soa=domain_search_result["soa"],
            www=domain_search_result["www"],
            ns=domain_search_result["ns"],
            txt=domain_search_result["txt"],
            ipv4=domain_search_result["ipv4"],
            ipv6=domain_search_result["ipv6"],
            asn=domain_search_result["asn"],
            xfr=domain_search_result["xfr"],
            ptr=domain_search_result["ptr"],
            registrar=domain_search_result["registrar"],
            expiration_date=domain_search_result["expiration_date"],
            srv=domain_search_result["srv"],
            email_exchange_service=domain_search_result["email_exchange_service"],
            o365=domain_search_result["o365"],
            has_https=domain_search_result["has_https"],
            is_blacklisted=domain_search_result["is_blacklisted"]
        )
        print(record)
        print(record.www)
        print(record.check_time)

        continue_ = False


if __name__ == "__main__":
    main()
