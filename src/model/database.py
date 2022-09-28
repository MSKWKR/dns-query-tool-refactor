from typing import Optional

from sqlalchemy import engine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel, create_engine, Session, select

from src.model.models import DNSRecord, Domain


# ------------------------------------------- database creation -------------------------------------------------------
def instantiate_engine(db_url: str, echo: bool = True) -> Optional[engine.Engine]:
    """
    Implicit function that instantiates the sqlalchemy database engine.

    :param db_url: Location for the database
    :type: str

    :param echo: The configuring logging parameter. if True, the connection pool will log informational output such as when connections are invalidated as well as when connections are recycled to the default log handler,
                 which defaults to sys.stdout for output. If set to the string "debug", the logging will include pool checkouts and checkins.
    :type: bool

    :return: The created engine if successful, else None
    :rtype: sqlalchemy.engine.Engine or None
    """
    new_engine = None
    try:
        new_engine = create_engine(db_url, echo=echo)
    except SQLAlchemyError as error:
        print(f"{error=}")

    return new_engine


def create_database_and_tables(db_engine: engine.Engine) -> None:
    """
    Function to create a database and create all the tables that were automatically registered in SQLModel.metadata
    to the given location

    :param db_engine: The database engine
    :type: str

    :return: None
    :rtype: None
    """

    SQLModel.metadata.create_all(db_engine)


# ------------------------------------------- database operation -------------------------------------------------------
def add_domain_data(db_engine: engine.Engine, data: any) -> None:
    """
    Add the given domain data to the database.

    :param db_engine: The connection engine for the database
    :type: engine.Engine

    :param data: The given class data object from the search result
    :type: any

    :return:
    :rtype: None
    """

    try:
        if not domain_name_exists(db_engine, data.domain_string):
            print("Adding to database.\n")
            with Session(db_engine) as session:
                session.add(data)
                session.commit()
                print("Added to database.\n")
        else:
            print("Domain Name Exists.")

    except SQLAlchemyError as error:
        print(f"{error=}")
        return


def add_domain_record_data(db_engine: engine.Engine, data: any) -> None:
    """
    Add the given domain data to the database.

    :param db_engine: The connection engine for the database
    :type: engine.Engine

    :param data: The given class data object from the search result
    :type: any

    :return:
    :rtype: None
    """

    try:
        print("Adding to database.\n")
        with Session(db_engine) as session:
            session.add(data)
            session.commit()
            print("Added to database.\n")

    except SQLAlchemyError as error:
        print(f"{error=}")
        return


def domain_name_exists(db_engine: engine.Engine, domain_name: str) -> bool:
    """"""
    with Session(db_engine) as session:
        statement = select(Domain).where(Domain.domain_string == domain_name)
        # Since there should be only one specific domain name in domain table, we fetch one
        result = session.exec(statement).one()
        return True if result else False


def read_data_from_domain_name(db_engine: engine.Engine, domain_name: str) -> Optional[DNSRecord]:
    try:
        with Session(db_engine) as session:
            statement = select(DNSRecord).where(DNSRecord.domain_name == domain_name)
            result = session.exec(statement).one()
            return result
    except SQLAlchemyError as error:
        print(f"Data reading error: {error}")
        return


def _main():
    pass


if __name__ == "__main__":
    _main()
