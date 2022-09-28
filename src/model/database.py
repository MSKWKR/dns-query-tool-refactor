from typing import Optional

from sqlalchemy import engine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel, create_engine, Session


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
def add_data(db_engine: engine.Engine, data: any) -> None:
    """
    Add the given data to the database.

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


def read_data(db_engine: engine.Engine):
    with Session(db_engine) as session:
        pass


def _main():
    pass


if __name__ == "__main__":
    _main()
