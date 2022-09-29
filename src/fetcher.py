from typing import Optional

from sqlalchemy_utils import database_exists

from src.model import models
from src.model.cache import RedisModel
from src.model.database import DomainDatabase
from src.model.models import DNSRecord
from src.model.utils import dictionary_value_to_bytes
from src.utils.tools import DNSToolBox


class DNSRecordFetcher:

    def __init__(self, domain_string: str, database_url: str):
        # setup toolbox
        self.toolbox = DNSToolBox()
        self.domain_string = self.toolbox.set_domain_string(domain_string)

        # setup database
        self.database_url = database_url
        self.database = DomainDatabase()
        self.database.set_db_url(database_url)
        self.database.instantiate_engine()

        # setup cache
        self._cache_info = {"host": "localhost", "port": 6379, "db_number": 0, "seconds": 30}
        self.cache_pool = RedisModel(
            host=self._cache_info["host"],
            port=self._cache_info["port"],
            db_number=self._cache_info["db_number"],
            seconds=self._cache_info["seconds"]
        )
        self.cache_pool.new_redis_client()

    def get_records(self) -> Optional[DNSRecord]:
        """
        Function that integrates all toolbox, database and caching logic. Get record for the needing domain

        :return: The cached search result
        :rtype: Optional[DNSRecord]
        """

        cached_result = self.cache_pool.get_value(key=self.domain_string)
        if not cached_result:
            # Check if it's in the database, if not then search with DNSToolBox
            if not self.database.domain_name_exists(domain_name=self.domain_string) or \
                    not self.database.record_timeout(domain_name=self.domain_string):

                # Search with toolbox
                domain = models.to_domain(self.domain_string)
                toolbox_search_result = dictionary_value_to_bytes(self.toolbox.domain_info)
                dns_record = models.to_DNS_record(toolbox_search_result)

                if not database_exists(url=self.database_url):
                    self.database.create_database_and_tables()

                # Add to database
                self.database.add_domain_data(domain_data=domain)
                self.database.add_domain_record_data(domain_record_data=dns_record)

                # Cache data
                self.cache_pool.set_value(key=self.domain_string, value=dns_record)

                # Return Result
                cached_result = self.cache_pool.get_value(key=self.domain_string)

            else:
                result = self.database.read_data_from_domain_name(domain_name=self.domain_string)
                # Cache data
                self.cache_pool.set_value(key=self.domain_string, value=result)

                # Return Result
                cached_result = self.cache_pool.get_value(key=self.domain_string)

        return cached_result

    # def get_record(self, record_type: str) -> any:
    #     pass
