import pickle
from datetime import timedelta
from typing import Optional

import redis
from redis.exceptions import ConnectionError


class RedisModel:
    """
    RedisModel handles caching data with key-value pairs
    """

    def __init__(self, host: str, port: int, db_number: int, password: str, seconds: int):
        self.client = None
        self._host = host
        self._port = port
        self._db = db_number
        self._password = password
        self.data_expiration_time = timedelta(seconds=seconds)

    def new_redis_client(self):
        """
        Util function for redis client instantiation, returns None if connection failed.

        :return: The initialized connection
        :rtype: Optional[redis.client.Redis]
        """
        try:
            client = redis.StrictRedis(
                host=self._host,
                port=self._port,
                db=self._db,
                password=self._password,
                # ssl=True,
                # ssl_cert_reqs='required',
                # ssl_ca_certs=""
            )
            print(client)
            print(client.ping())
            ping = client.ping()
            if ping:
                self.client = client


        except (redis.AuthenticationError, ConnectionError) as error:
            print(f"Redis server connection error: {error}")

    def set_value(self, key: str, value: any) -> bool:
        """
        Setting a key-value pair within the cache pool. Will pickle the input value first.

        :param key: The key for the value to store
        :type: str

        :param value: Object to store along with the key
        :type: any

        :return: True if successfully set, else False
        :rtype: False
        """

        state = False
        try:
            # Serialize first since data need to be bytes to be set in Redis
            value = pickle.dumps(value)

            state = self.client.set(
                name=key,
                ex=self.data_expiration_time,
                value=value,
            )
            print("Added to Cache")
        except redis.exceptions.DataError as error:
            print(f"Redis Error: {error}")

        return state

    def get_value(self, key: str) -> Optional[any]:
        """
        Takes the given key and return the unpickled object, None if value doesn't exist.

        :param key: The key value to search within the cache pool.
        :type: str

        :return: The retrieved value
        :rtype: Optional[any]
        """
        value = self.client.get(key)
        if value:
            value = pickle.loads(value)

        return value


def _main():
    r = RedisModel(
        host="dnstool.redis.cache.windows.net",
        port=6379,
        password="CU6WkddvYT62X6rvuPZmJftgQFENodV4kAzCaPUCHoM=",
        db_number=0,
        seconds=30
    )

    r.new_redis_client()


if __name__ == "__main__":
    _main()
