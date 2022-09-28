from sqlalchemy_utils import database_exists

from src.model import database, models, utils
from src.utils.tools import DNSToolBox

sqlite_file_name = "domain_record.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


def main():
    toolbox = DNSToolBox()
    continue_ = True

    while continue_:
        domain_to_check = input("Enter Domain Name: ")

        toolbox.set_domain_string(domain_to_check)
        print("Fetching Records...")

        domain = models.to_domain(domain_to_check)

        search_result = toolbox.domain_info
        domain_search_result = utils.dictionary_value_to_bytes(search_result=search_result)
        dns_record = models.to_DNS_record(domain_search_result)
        print("Records Fetched.\n")

        engine = database.instantiate_engine(db_url=sqlite_url)
        if not database_exists(url=sqlite_url):
            database.create_database_and_tables(engine)

        # Do nothing if domain exists
        database.add_domain_data(db_engine=engine, data=domain)
        # Will still add the domain search record
        database.add_domain_record_data(db_engine=engine, data=dns_record)

        a = database.read_data_from_domain_name(engine, "google.com")
        print(a.domain_name, a.search_used_time)
        print(utils.bytes_decrypt(a.a))

        if input("Do you want to continue? (y/n)").lower() == "n":
            continue_ = False


if __name__ == "__main__":
    main()
