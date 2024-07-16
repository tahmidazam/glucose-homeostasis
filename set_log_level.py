import argparse
import logging

from string_to_log_level import string_to_log_level


def set_log_level(level: str):
    log_level: int = string_to_log_level(level)
    logging.getLogger().setLevel(log_level)
    logging.info(f"Log level set to {logging.getLevelName(log_level)}.")
