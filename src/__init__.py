from src.model import models
from src.model.cache import RedisModel
from src.model.database import DomainDatabase
from src.model.models import DNSRecord
from src.model.utils import dictionary_value_to_bytes, bytes_decrypt
from src.utils.tools import DNSToolBox

# Database Information
sqlite_file_name = "domain_record.db"
dns_database_url = f"sqlite:///src/{sqlite_file_name}"

# Cacher Server Information
dns_cache_server_info = {
    "host": "localhost",
    "port": 6379,
    "db_number": 0,
    "seconds": 30
}

# Setup Database
dns_database = DomainDatabase()
dns_database.set_db_url(dns_database_url)
dns_database.instantiate_engine(echo=False)

# Setup Cache Pool
dns_cache_pool = RedisModel(
    host=dns_cache_server_info["host"],
    port=dns_cache_server_info["port"],
    db_number=dns_cache_server_info["db_number"],
    seconds=dns_cache_server_info["seconds"]
)
dns_cache_pool.new_redis_client()

# Setup DNSToolBox
toolbox = DNSToolBox()
