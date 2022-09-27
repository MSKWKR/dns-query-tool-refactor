from pprint import pprint

from sqlmodel import create_engine, SQLModel, Session

from src.model.models import to_domain, to_DNS_record
from src.utils.tools import DNSToolBox


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
        domain_info = to_domain(domain_to_check)
        a = toolbox.domain_info
        pprint(a)
        dns_record = to_DNS_record(a)

        print("Records Fetched")

        engine = create_engine("sqlite:///database.db")
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            session.add(domain_info)
            # session.add(dns_record)
            session.commit()

        continue_ = False


if __name__ == "__main__":
    main()
