import logging

LOGGER_NAME = 'Scanner {scanner_id}'
LOG_PATH = 'scanners.log'
LOG_FORMAT = '[%(asctime)s] [%(name)s] [%(levelname)s] -> %(message)s'


def setup_logger(logger_id: int) -> logging.Logger:
    """
    Setup logger for scanner.

    :param logger_id: Logger id.
    :return: Logger instance.
    """
    logger = logging.getLogger(name=LOGGER_NAME.format(scanner_id=logger_id))
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)
    stream_handler = create_stream_handler(formatter=formatter)
    file_handler = create_file_handler(formatter=formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def create_stream_handler(
        formatter: logging.Formatter) -> logging.StreamHandler:
    """
    Create stream handler for logger.

    :param formatter: Data format.
    :return: Stream handler.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    return stream_handler


def create_file_handler(formatter: logging.Formatter) -> logging.FileHandler:
    """
    Create file handler for logger.

    :param formatter: Data format.
    :return: File handler.
    """
    file_handler = logging.FileHandler(filename=LOG_PATH)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    return file_handler
