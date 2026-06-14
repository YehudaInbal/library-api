from logger import get_logger
from database.connection_db import get_connection
from fastapi import HTTPException
from database import member_db


logger = get_logger(__name__)

BOOK_VALUES = ["genre", "author", "title", "is_available"]
GENRES = ('Non-Fiction', 'Science', 'History', 'Other','Fiction')



class BookDB:

            
    @staticmethod
    def add_book(data: dict) -> int:
        connection = None
        for k in data.keys():
            if k not in BOOK_VALUES:
                logger.warning(f"{k}Not in book allowed fields")
                raise KeyError(f"{k}Not in book allowed fields")
        for k in BOOK_VALUES:
            if k not in data.keys() and k != "is_available":
                logger.warning(f"{k} missing in book data")
                raise KeyError(f"{k} missing in book data")
        if data["genre"] not in GENRES:
            logger.warning(f"{data['genre']} not in allowed genre")
            raise KeyError(f"{data['genre']} not in allowed genre")
        try:
            logger.info("starting to insert a book")
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO books(title, author, genre)
            VALUES(%(title)s, %(author)s, %(genre)s)""", data)
            connection.commit()
            logger.info("book saved successfully")
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
            logger.info("Pulls all books from the database")
            cursor.execute("SELECT * FROM books")
            logger.info("The processing of the books table has ended.")
            return cursor.fetchall()
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    @staticmethod
    def get_book_by_id(id:int) -> dict:
        conn =None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            logger.info("looking for book")
            cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
            logger.info("proses end successfully")
            return cursor.fetchone()
        finally:
            if conn:
                cursor.close()
                conn.close()
        
    @staticmethod
    def update_book(data:dict, book_id:int) -> bool:
        conn = None
        book = BookDB.get_book_by_id(book_id)
        if not book:
            logger.warning("No matching id")
            raise ValueError("No matching id")
        for k in data:
            if k not in BOOK_VALUES:
                logger.warning(f"Error of entering an inappropriate value({k}) prevented")
                raise KeyError(f"{k} Not in allowed filled")
            if 'genre' in  data.keys():
                if data['genre'] not in GENRES:
                    logger.warning(f"Error of entering an inappropriate value({data['genre']}) to genre prevented")
                    raise KeyError(f"{data['genre']} Not in allowed genre")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("updating the book")
            for k, v in data.items():
                cursor.execute(f"UPDATE books SET {k} = %s WHERE id = %s", (v, book_id))
            conn.commit()
            logger.info("book change successfully")
            return cursor.rowcount
        finally:
            if conn:
                cursor.close()
                conn.close()
        
    @staticmethod
    def borrow_book(book_id, member_id) -> int:
        conn =None
        book = BookDB.get_book_by_id(book_id)
        if not book:
            logger.warning("status code = 404")
            raise HTTPException(status_code=404, detail="book not found")
        member = member_db.Members.get_member_by_id(member_id)
        if not member:
            logger.warning("status code = 404")
            raise HTTPException(status_code=404, detail="member not found")
        if member['total_borrows'] >= 3:
            logger.warning(f"{member_id} cannot borrow more than 3 books")
            raise HTTPException(status_code=400, detail="You cannot borrow more than 3 books.")
        if member['is_active'] != True:
            logger.warning(f"member ({member}) is not active")
            raise HTTPException(status_code=400, detail="member is not active")
        if book['is_available'] != True:
            logger.warning(f"{book_id} is not available")
            raise HTTPException(status_code=400, detail="Book is not available")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("borroing_book")
            cursor.execute("UPDATE books SET is_available = false WHERE id = %s", (book_id,))
            cursor.execute("UPDATE books SET borrowed_by_member_id = %s WHERE id = %s", (member_id, book_id))
            logger.info("update in books, waiting to members")
            member_db.Members.increment_borrows(member_id)
            conn.commit()
            return cursor.rowcount
        finally:
            if conn:
                cursor.close()
                conn.close()

    @staticmethod
    def return_book(book_id, member_id):
        conn =None
        book = BookDB.get_book_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="book not found")
        member = member_db.Members.get_member_by_id(member_id)
        if not member:
            raise HTTPException(status_code=404, detail="member not found")
        if book['borrowed_by_member_id'] != member_id:
            logger.warning("An attempt to return a book not in the customer's possession was blocked.")
            raise HTTPException(status_code=422, detail="You can only return books teat you borrowed.")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("returning book")
            cursor.execute("UPDATE books SET is_available = True WHERE id = %s", (book_id,))
            cursor.execute("UPDATE books SET borrowed_by_member_id = null WHERE id = %s", (book_id,))
            logger.info("books Ok waiting for members")
            member_db.Members.decrement_borrows(member_id)
            conn.commit()
            return cursor.rowcount
        finally:
            if conn:
                cursor.close()
                conn.close()

    @staticmethod
    def count_books_total():
        conn =None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("counting books")
            cursor.execute("SELECT COUNT(*) FROM books")
            logger.info("summarizes")
            return cursor.fetchall()[0][0]
        finally:
            if conn:
                cursor.close()
                conn.close()


    @staticmethod
    def count_available_books():
        conn =None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("counting available books")
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = true")
            logger.info("summarizes")
            return cursor.fetchall()[0][0]
        finally:
            if conn:
                cursor.close()
                conn.close()
    

    @staticmethod
    def count_borrowed_books():
        conn =None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("counting borrowed books")
            cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = false")
            logger.info("summarizes")
            return cursor.fetchall()[0][0]
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    @staticmethod
    def count_by_genre(genre) -> int:
        conn =None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("counting books")
            cursor.execute("SELECT COUNT(*) FROM books WHERE genre = %s", (genre,))
            logger.info(f"summarizes {genre}")
            return cursor.fetchall()[0][0]
        finally:
            if conn:
                cursor.close()
                conn.close()

    @staticmethod
    def count_active_borrows_by_member(member_id):
        conn =None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("counting active borrows")
            cursor.execute("SELECT COUNT(*) FROM books WHERE borrowed_by_member_id = %s", (member_id,))
            logger.info("summarizes active_borrows")
            return cursor.fetchall()[0][0]
        finally:
            if conn:
                cursor.close()
                conn.close()