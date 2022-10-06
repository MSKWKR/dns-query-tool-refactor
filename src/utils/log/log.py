import logging
from functools import wraps


def create_logger() -> logging.Logger:
    # create a logger object
    new_logger = logging.getLogger('execution_log')
    new_logger.setLevel(logging.INFO)

    # create a file to store all the logged exceptions
    logfile = logging.FileHandler('./execution_log.log')

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)

    logfile.setFormatter(formatter)
    new_logger.addHandler(logfile)

    return new_logger


def exception(py_logger: logging.Logger):
    # logger is the logging object
    # exception is the decorator objects
    # that logs every exception into log file
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                issue = f"exception in {func.__name__}\n"
                issue += "------------------------------------------------------------\n"
                py_logger.exception(issue)

        return wrapper

    return decorator


# Create a global logger object
LOGGER = create_logger()
