from datetime import datetime, timedelta
from typing import Optional

import sqlalchemy.exc
from sqlalchemy import engine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel, create_engine, Session, select

from src.model.models import DNSRecord, Domain


class DomainDatabase:
    """
    DomainDatabase handles operations for sqlite3
    """

    def __init__(self):
        self.db_engine = None
        self._db_url = None

    # ------------------------------------------- database creation -------------------------------------------------------
    def set_db_url(self, url: str):
        self._db_url = url

    def instantiate_engine(self, echo: bool = True) -> Optional[engine.Engine]:
        """
        Function that instantiates the sqlalchemy database engine.

        :param echo: The configuring logging parameter. if True, the connection pool will log informational output such as when connections are invalidated as well as when connections are recycled to the default log handler,
                     which defaults to sys.stdout for output. If set to the string "debug", the logging will include pool checkouts and checkins.
        :type: bool

        :return: The created engine if successful, else None
        :rtype: sqlalchemy.engine.Engine or None
        """
        new_engine = None
        try:
            new_engine = create_engine(self._db_url, echo=echo)
        except SQLAlchemyError as error:
            print(f"{error=}")

        self.db_engine = new_engine
        return self.db_engine

    def create_database_and_tables(self) -> None:
        """
        Function to create a database and create all the tables that were automatically registered in SQLModel.metadata
        to the given location

        :return: None
        :rtype: None
        """

        SQLModel.metadata.create_all(self.db_engine)

    # ------------------------------------------- database operation -------------------------------------------------------
    def add_domain_data(self, domain_data: Domain) -> None:
        """
        Add the given domain data to the database.

        :param domain_data: The given class data object from the search result
        :type: any

        :return:
        :rtype: None
        """

        try:
            if not self.domain_name_exists(domain_data.domain_string):
                print("Adding to database.\n")
                with Session(self.db_engine) as session:
                    session.add(domain_data)
                    session.commit()
                    print("Added to database.\n")
            else:
                print("Domain Name Exists.")

        except SQLAlchemyError as error:
            print(f"{error=}")
            return

    def add_domain_record_data(self, domain_record_data: DNSRecord) -> None:
        """
        Add the given domain data to the database.

        :param domain_record_data: The given class data object from the search result
        :type: DNS

        :return:
        :rtype: None
        """
        domain_record_data.domain_id = self.get_domain_id(domain_record_data.domain_name)
        try:
            print("Adding to database.\n")
            with Session(self.db_engine) as session:
                session.add(domain_record_data)
                session.commit()
                print("Added to database.\n")

        except SQLAlchemyError as error:
            print(f"{error=}")
            return

    def domain_name_exists(self, domain_name: str) -> bool:
        """
        Util checking whether the domain name exists within table Domain
        :param domain_name: Domain string
        :type: str

        :return: True if exists else False
        :rtype: bool
        """

        with Session(self.db_engine) as session:
            statement = select(Domain).where(Domain.domain_string == domain_name)
            # Since there should be only one specific domain name in domain table, we fetch one
            result = None
            try:
                result = session.exec(statement).one()
            except sqlalchemy.exc.NoResultFound:
                print(f"Record data with domain name: {domain_name} doesn't exist")

            return True if result else False

    def read_data_from_domain_name(self, domain_name: str) -> Optional[DNSRecord]:
        """
        Function to read the latest data with the given input domain

        :param domain_name: Domain string
        :type: str

        :return: The latest fetched result
        :rtype: Optional[DNSRecord]
        """
        try:
            with Session(self.db_engine) as session:
                statement = select(DNSRecord).where(DNSRecord.domain_name == domain_name)
                result = session.exec(statement).all()
                return result[-1]
        except SQLAlchemyError as error:
            print(f"Data reading error: {error}")
            return

    def get_domain_id(self, domain_name: str) -> int:
        """
        Helper function for checking domain id from the Domain table

        :param domain_name:Domain string
        :type: str

        :return: The domain id
        :rtype: int
        """
        with Session(self.db_engine) as session:
            statement = select(Domain).where(Domain.domain_string == domain_name)
            result = session.exec(statement).one()
            return result.id

    def get_last_record_search_time(self, domain_name: str) -> Optional[str]:
        """
        Helper function to fetch the last search time for the latest record within database

        :param domain_name: Domain string
        :type: str

        :return: String format of the last check time
        :rtype: str
        """
        last_check = None
        try:
            with Session(self.db_engine) as session:
                statement = select(DNSRecord).where(DNSRecord.domain_name == domain_name)
                last_result = session.exec(statement).all()[-1]
                last_check = last_result.check_time

        except sqlalchemy.exc.NoResultFound:
            print(f"Record data with domain name: {domain_name} doesn't exist")

        return last_check

    def record_timeout(self, domain_name: str) -> bool:
        """
        Check if record within database isn't up-to-date

        :param domain_name: Domain string
        :type: str

        :return: True if data isn't up-to-date, else False
        :rtype: bool
        """
        now = datetime.now()  # pytz.timezone("Asia/Taipei"))
        last_record_search_time = datetime.strptime(self.get_last_record_search_time(domain_name=domain_name),
                                                    "%Y-%m-%d %H:%M:%S")

        pass_time = (now - last_record_search_time).seconds
        expire_time = timedelta(minutes=5).seconds

        # time to live
        ttl = expire_time - pass_time
        print(f"{ttl=}")

        # Possible bug here, might use within different timezone
        if ttl <= 0:
            return True

        return False

    def read_dns_record(self, input_record: DNSRecord) -> dict:
        """
        Function to read from the fetched database value
        :param input_record: The result fetched from the database
        :type: DNSRecord

        :return: The transformed dictionary
        :rtype: dict
        """
        with Session(self.db_engine):
            record = input_record
            result = {
                "domain_name": record.domain_name,
                "check_time": record.check_time,
                "a": record.a,
                "aaaa": record.aaaa,
                "mx": record.mx,
                "soa": record.soa,
                "www": record.www,
                "ns": record.ns,
                "txt": record.txt,
                "ipv4": record.ipv4,
                "ipv6": record.ipv6,
                "asn": record.asn,
                "xfr": record.xfr,
                "ptr": record.ptr,
                "registrar": record.registrar,
                "expiration_date": record.expiration_date,
                "email_exchange_service": record.email_exchange_service,
                "srv": record.srv,
                "o365": record.o365,
                "has_https": record.has_https,
                "is_blacklisted": record.is_blacklisted
            }
            return result


def _main():
    d = DomainDatabase()
    d.set_db_url(f"sqlite:///../../domain_record.db")
    d.instantiate_engine()
    print(d.get_domain_id("python.org"))

    print(d.get_last_record_search_time("python.org"))
    print(f"timeout: {d.record_timeout('python.org')}")
    a = d.read_data_from_domain_name("python.org")
    print(d.read_dns_record(a))


if __name__ == "__main__":
    _main()
