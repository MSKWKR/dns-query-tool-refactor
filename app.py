from sqlalchemy_utils import database_exists

from src.model import database, models, utils
from src.utils.tools import DNSToolBox

sqlite_file_name = "domain_record.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


def main():
    toolbox = DNSToolBox()
    continue_ = True
    #
    # sqlite_file_name = "database.db"
    # sqlite_url = f"sqlite:///{sqlite_file_name}"
    # domain_database_engine = database.instantiate_engine(sqlite_url)

    while continue_:
        domain_to_check = input("Enter Domain Name: ")

        toolbox.set_domain_string(domain_to_check)
        print("Fetching Records...")

        domain = models.to_domain(domain_to_check)
        domain_search_result = utils.dictionary_value_to_bytes(search_result=toolbox.domain_info)
        dns_record = models.to_DNS_record(domain_search_result)
        print("Records Fetched.\n")
        print("Adding to database.\n")

        engine = database.instantiate_engine(db_url=sqlite_url)
        if not database_exists(url=sqlite_url):
            database.create_database_and_tables(engine)

        database.add_data(db_engine=engine, data=domain)
        database.add_data(db_engine=engine, data=dns_record)
        print("Added to database.\n")

        if input("Do you want to continue? (y/n)").lower() == "n":
            continue_ = False


if __name__ == "__main__":
    main()
