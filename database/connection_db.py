import mysql.connector
from logger import get_logger

logger = get_logger(__name__)


def get_connection():
    try:
        return mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='secret',
            database='library_db'
        )
    except Exception as e:
        logger.warning(e)
        raise