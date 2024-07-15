import logging


def string_to_log_level(string: str) -> int:
    """
    Converts a string to a logging level.
    :param string: The string to convert.
    :return: The logging level.
    """
    match string.lower():
        case "debug":
            return logging.DEBUG
        case "info":
            return logging.INFO
        case "warning":
            return logging.WARNING
        case "error":
            return logging.ERROR
        case "critical":
            return logging.CRITICAL
        case _:
            return logging.WARNING
