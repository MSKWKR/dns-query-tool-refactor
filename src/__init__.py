import logging
from datetime import datetime

from src.model import models
from src.model.cache import RedisModel
from src.model.database import DomainDatabase
from src.model.models import DNSRecord
from src.model.utils import dictionary_value_to_bytes, bytes_decrypt
from src.utils.log.log import LOGGER
from src.utils.tools import DNSToolBox

LOGGER.log(level=logging.INFO,
           msg=f"---------------- DNS Search {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ----------------\n\n")

# Database Information
sqlite_file_name = "domain_record.db"
dns_database_url = f"sqlite:///{sqlite_file_name}"

# Cacher Server Information
dns_cache_server_info = {
    # Connect to Azure Redis Cache
    "host": "dnstool.redis.cache.windows.net",
    "port": 6379,
    "db_number": 0,
    "seconds": 600,
    "password": "CU6WkddvYT62X6rvuPZmJftgQFENodV4kAzCaPUCHoM="
}

# Setup Database
dns_database = DomainDatabase()
dns_database.set_db_url(dns_database_url)
dns_database.instantiate_engine(echo=False)
# Clean outdated records
dns_database.clean_outdated_records()

# Setup Cache Pool
dns_cache_pool = RedisModel(
    host=dns_cache_server_info["host"],
    port=dns_cache_server_info["port"],
    db_number=dns_cache_server_info["db_number"],
    seconds=dns_cache_server_info["seconds"],
    password=dns_cache_server_info["password"]
)
dns_cache_pool.new_redis_client()

# Setup DNSToolBox
toolbox = DNSToolBox()
