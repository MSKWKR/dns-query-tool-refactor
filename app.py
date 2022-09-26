# from src import database, models
from pprint import pprint

from src.utils.tools import DNSToolBox


#
#
# class Domain(models.Domain, table=True):
#     pass
#
#
# class DNSRecord(models.Domain, table=True):
#     pass
#

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
        pprint(toolbox.domain_info)
        continue_ = False


if __name__ == "__main__":
    main()
