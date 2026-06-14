import logging
from logging import Logger

LOGS_FILE = "logs/app.log"


def get_logger(name: str) -> Logger:
    return logging.basicConfig(
        level=logging.INFO,
        filename=LOGS_FILE,
        format=("%(asctime)s | %(levelname)s | %(message)s | %(name)s"))