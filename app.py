from pprint import pprint

from src.fetcher import get_records


def main():
    test_d = "google.com"
    a = get_records(test_d)
    pprint(a)


if __name__ == "__main__":
    main()
