from pprint import pprint

from src import fetcher
from src.model.utils import result_decrypt

sqlite_file_name = "domain_record.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


def main():
    test_d = "yahoo.com"
    test_fetcher = fetcher.DNSRecordFetcher(test_d, sqlite_url)
    a = test_fetcher.get_records()
    result_decrypt(a)
    pprint(a)
    print("\n")
    print(test_fetcher.get_record("a"))


if __name__ == "__main__":
    main()
