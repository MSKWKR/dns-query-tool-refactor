from sqlalchemy_utils import database_exists

from src.model import database, models, utils
from src.utils.tools import DNSToolBox

sqlite_file_name = "domain_record.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


def main():
    toolbox = DNSToolBox()
    domain_database = database.DomainDatabase()
    domain_database.set_db_url(url=sqlite_url)
    domain_database.db_engine = domain_database.instantiate_engine()

    test_domains = [
        # "example.com", "freedom.net.tw", "google.com", "python.org", "freedom.net.tw", "google.com", "python.org"
        "google.com",
    ]
    for domain in test_domains:

        domain_to_check = domain
        toolbox.set_domain_string(domain_to_check)

        print(f"Fetching Records: {domain}")
        # Add to domain table
        domain = models.to_domain(domain_to_check)
        search_result = toolbox.domain_info
        # Data serializing
        domain_search_result = utils.dictionary_value_to_bytes(search_result=search_result)
        # Add to dns record table
        dns_record = models.to_DNS_record(domain_search_result)
        print("Records Fetched.\n")

        if not database_exists(url=sqlite_url):
            domain_database.create_database_and_tables()

        # Do nothing if domain exists
        domain_database.add_domain_data(domain_data=domain)
        # Will still add the domain search record
        domain_database.add_domain_record_data(domain_record_data=dns_record)

        # print(f"Used time: {domain_database.read_data_from_domain_name(domain).search_used_time}")


if __name__ == "__main__":
    main()
