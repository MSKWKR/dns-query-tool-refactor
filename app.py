from src import fetcher

sqlite_file_name = "domain_record.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


def main():
    test_d = "google.com"
    test_fetcher = fetcher.DNSRecordFetcher(test_d, sqlite_url)
    a = test_fetcher.get_records()
    print(type(a))


if __name__ == "__main__":
    main()
