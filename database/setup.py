from connection import get_connection
from logger import get_logger


logger = get_logger(__name__)




CREATE_BOOKS_TABLE =  """
    CREATE TABLE IF NOT EXIST books(
    "id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL,
    author VARCHAR(5) NOT NULL,
    genre ENUM('Non-Fiction', 'Science', 'History', 'Other') NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    borrowed_by_member_id INT DEFAULT NULL
    )
"""

CREATE_MEMBERS_TABLE = """
    CREATE TABLE IF NOT EXIST members(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(250) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    total_borrows INT DEFAULT 0
    )
"""

def setup():
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        logger.info("starting to create table")
        cursor.execute(CREATE_BOOKS_TABLE)
        cursor.execute(CREATE_MEMBERS_TABLE)
        connection.commit()
        logger.info("Tables created successfully")
    except Exception as e:
        logger.warning(f"Setup fail! {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
