from logger import get_logger
from database.connection_db import get_connection


Logger = get_logger(__name__)

BOOK_VALUES = ["genre", "author", "title", "is_available"]
GENRES = ('Non-Fiction', 'Science', 'History', 'Other','Fiction')
MEMBER_VALUES = ("is_active", "email", "name")


class BookDB():

            
    @staticmethod
    def add_book(data: dict) -> int:
        connection = None
        for k in data.keys():
            if k not in BOOK_VALUES:
                Logger.warning(f"{k}Not in book allowed fields")
                raise KeyError(f"{k}Not in book allowed fields")
        for k in BOOK_VALUES:
            if k not in data.keys() and k != "is_available":
                Logger.warning(f"{k} missing in book data")
                raise KeyError(f"{k} missing in book data")
        if data["genre"] not in GENRES:
            Logger.warning(f"{data['genre']} not in allowed genre")
            raise KeyError(f"{data['genre']} not in allowed genre")
        try:
            Logger.info("starting to insert a book")
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO books(title, author, genre)
            VALUES(%(title)s, %(author)s, %(genre)s)""", data)
            connection.commit()
            Logger.info("book saved successfully")
            return cursor.lastrowid
        finally:
            if connection:
                cursor.close()
                connection.close()

    @staticmethod
    def get_all_book() -> list:
        cunn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            Logger.info("Pulls all books from the database")
            cursor.execute("SELECT * FROM books")
            Logger.info("The processing of the books table has ended.")
            return cursor.fetchall()
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    @staticmethod
    def get_book_by_id(id:int) -> dict:
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            Logger.info("looking for book")
            cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
            Logger.info("proses end successfully")
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
        
    @staticmethod
    def update_book(data:dict, book_id:int) -> bool:
        conn = None
        book = BookDB.get_book_by_id(book_id)
        if not book:
            Logger.warning("No matching id")
            raise ValueError("No matching id")
        for k in data:
            if k not in BOOK_VALUES:
                Logger.warning(f"Error of entering an inappropriate value({k}) prevented")
                raise KeyError(f"{k} Not in allowed filled")
            if 'genre' in  data.keys():
                if data['genre'] not in GENRES:
                    Logger.warning(f"Error of entering an inappropriate value({data['genre']}) to genre prevented")
                    raise KeyError(f"{data['genre']} Not in allowed genre")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            Logger.info("updating the book")
            for k, v in data.items():
                cursor.execute(f"UPDATE books SET {k} = %s WHERE id = %s", (v, book_id))
            conn.commit()
            Logger.info("book change successfully")
            return cursor.rowcount
        finally:
            if conn:
                cursor.close()
                conn.close()
        
    @staticmethod
    def borrow_book(book_id, member_id):
        pass


    @staticmethod
    def return_book(book_id, member_id):
        pass