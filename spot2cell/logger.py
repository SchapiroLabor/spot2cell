import logging
import sys


def set_logger(logger=None,
               log_level='info',
               log_format='%(asctime)s - %(levelname)s - %(message)s'):
    """ Function to set up the handle error logging.

    logger (obj) = a logger object (optional, creates a default logger if not provided)
    log_level (str) = level of information to print out, options are {info, debug} [Default: info]
    log_format (str) = format of the log messages [Default: '%(asctime)s - %(levelname)s - %(message)s']

    """
    # Create a default logger if not provided
    if logger is None:
        logger = logging.getLogger(__name__)

    # Determine log level
    if log_level == 'info':
        _level = logging.INFO
    elif log_level == 'debug':
        _level = logging.DEBUG
    else:
        raise ValueError(f"Log level {log_level} not recognized.")

    # Set the level in logger
    logger.setLevel(_level)

    # Set the log format
    logfmt = logging.Formatter(log_format)

    # Set logger output to STDOUT and STDERR
    log_handler = logging.StreamHandler(stream=sys.stdout)
    log_handler.setLevel(_level)
    log_handler.setFormatter(logfmt)

    error_handler = logging.StreamHandler(stream=sys.stderr)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logfmt)

    # Add handler to the main logger
    logger.addHandler(log_handler)
    logger.addHandler(error_handler)

    return logger
