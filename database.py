from typing import Optional

from sqlalchemy import engine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel, create_engine


def _instantiate_engine(db_url: str, echo: bool = True) -> Optional[engine.Engine]:
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


def create_database_and_tables(db_url: str) -> None:
    """
    Function to create a database and create all the tables that were automatically registered in SQLModel.metadata
    to the given location

    :param db_url: Location for the database
    :type: str

    :return: None
    :rtype: None
    """

    new_engine = _instantiate_engine(db_url)
    if new_engine:
        SQLModel.metadata.create_all(new_engine)


def _main():
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    create_database_and_tables(sqlite_url)


if __name__ == "__main__":
    _main()
