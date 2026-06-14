import logging


LOGS_FILE = "logs/app.log"


def get_logger(name: str):
    logging.basicConfig(
        level=logging.INFO,
        filename=LOGS_FILE,
        format="%(asctime)s | %(levelname)s | %(message)s | %(name)s")
    return logging.getLogger(name)