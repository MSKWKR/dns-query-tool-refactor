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

        return new_engine

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
        """"""
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
        with Session(self.db_engine) as session:
            statement = select(Domain).where(Domain.domain_string == domain_name)
            result = session.exec(statement).one()
            return result.id


def _main():
    pass


if __name__ == "__main__":
    _main()
