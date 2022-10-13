import json
from typing import Optional

from sqlalchemy_utils import database_exists

from src.model import models
from src.model.utils import dictionary_value_to_bytes, result_decrypt
from . import toolbox, dns_database, dns_cache_pool, dns_database_url


def get_records(domain_string: str) -> dict:
    """
    Function that integrates all toolbox, database and caching logic. Get record for the needing domain

    :return: The cached search result
    :rtype: Optional[DNSRecord]
    """
    toolbox.set_domain_string(domain_string=domain_string)

    if not database_exists(url=dns_database_url):
        dns_database.create_database_and_tables()

    cached_result = dns_cache_pool.get_value(key=domain_string)
    if not cached_result:
        # Check if it's in the database, if not in or timeout then search with DNSToolBox
        if not dns_database.domain_name_exists(domain_name=domain_string) or not dns_database.domain_record_exists(
                domain_name=domain_string) or dns_database.record_timeout(domain_name=domain_string):

            # Search with toolbox
            domain = models.to_domain(domain_string)
            toolbox_search_result = dictionary_value_to_bytes(toolbox.domain_info)
            dns_record = models.to_DNS_record(toolbox_search_result)

            # Add to database
            dns_database.add_domain_data(domain_data=domain)
            dns_database.add_domain_record_data(domain_record_data=dns_record)

            # Cache data
            dns_cache_pool.set_value(key=domain_string, value=toolbox_search_result)

            # Return Result
            cached_result = dns_cache_pool.get_value(key=domain_string)

        else:
            # Read from database
            database_result = dns_database.read_data_from_domain_name(domain_name=domain_string)

            # Transfer database object to normal dictionary
            result = dns_database.read_dns_record(input_record=database_result)

            # Cache data
            dns_cache_pool.set_value(key=domain_string, value=result)

            # Return Result
            cached_result = dns_cache_pool.get_value(key=domain_string)

    # Ultimately return the cached result
    result_decrypt(cached_result)
    # cached_result = json.dumps(cached_result)
    # print(type(cached_result))
    return cached_result


def get_human_readable_records(domain_string: str) -> dict:
    pass


def get_record(domain_string: str, record_type: str) -> Optional[any]:
    """
    Get the specific record from the results with the given type

    :param domain_string: Domain to check
    :type:: str

    :param record_type: DNS record type
    :type: str

    :return: The specific field value
    :rtype: any
    """
    record_type = record_type.lower()
    data = get_records(domain_string)
    if not data.get(record_type):
        return None
    else:
        record_value = data[record_type]
        return record_value


def get_record_to_json(domain_string: str, file_name: str):
    """
    Function to dump all the fetched result to a json file


    :param domain_string: Domain to check

    :param file_name: The file name

    :return:
    """
    result = get_records(domain_string=domain_string)

    with open(f"../{file_name}.json", "w", encoding="utf-8") as file:
        json.dump(result, file)
