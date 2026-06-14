from logger import get_logger
from database.connection_db import get_connection
from mysql.connector.errors import IntegrityError

logger = get_logger(__name__)


MEMBER_VALUES = ("is_active", "email", "name")


class Members:

    
    @staticmethod
    def add_member(data: dict) -> int:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("starting to insert a member")
            cursor.execute("""INSERT INTO members(email, name)
            VALUES (%(email)s, %(name)s)""", data)
            conn.commit()
            logger.info("New member set")
            return cursor.lastrowid
        except IntegrityError as e:
            logger.warning(f"Email already exist {e}")
            raise ValueError(f"{e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_members() -> list:
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            logger.info("Looking for members")
            cursor.execute("SELECT * FROM members")
            logger.info("finish looking for members")
            return cursor.fetchall()
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    @staticmethod
    def get_member_by_id(id:int):
        conn =None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            logger.info("Finding member")
            cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
            logger.info("search ending")
            return cursor.fetchone()
        finally:
            if conn:
                cursor.close()
                conn.close()
        
    @staticmethod
    def update_member(data: dict, id_member) -> int:
        conn = None
        for k in data.keys():
            if k not in MEMBER_VALUES:
                logger.warning(f"Error of entering an inappropriate value({k}) prevented")
                raise ValueError(f"{k} not in allowed filed")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("starring to update")
            for k, v in data.items():
                cursor.execute(f"UPDATE members SET {k} = %s WHERE id = %s", (v, id_member))
            conn.commit()
            logger.info("member update successfully")
            return cursor.rowcount
        except IntegrityError as e:
            logger.warning(f"Email already exist {e}")
            raise KeyError(f"{e}")
        finally:
            if conn:
                cursor.close()
                conn.close
    


    @staticmethod
    def deactivate_member(id):
        member = Members.get_member_by_id(id)
        if not member:
            raise ValueError
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("Starting to deactivate_member")
            cursor.execute("UPDATE members SET is_active = false WHERE id = %s", (id,))
            logger.info("Finish to deactivate_member")
            conn.commit()
            return cursor.rowcount
        finally:
            if conn:
                cursor.close()
                conn.close()
        
    
    @staticmethod
    def activate_member(id):
        member = Members.get_member_by_id(id)
        if not member:
            raise ValueError
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("Starting to deactivate_member")
            cursor.execute("UPDATE members SET is_active = true WHERE id = %s", (id,))
            logger.info("Finish to deactivate_member")
            conn.commit()
            return cursor.rowcount
        finally:
            if conn:
                cursor.close()
                conn.close()


    @staticmethod
    def increment_borrows(id) -> int:
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT total_borrows FROM members WHERE id = %s", (id,))
            set_borrows = cursor.fetchone()['total_borrows'] + 1
            logger.info(f"incrising member borrows ({set_borrows - 1} -> {set_borrows})")
            cursor.execute("UPDATE members SET total_borrows = %s WHERE id = %s", (set_borrows, id))
            conn.commit()
            logger.info("member update")
            return set_borrows
        finally:
            if conn:
                cursor.close()
                conn.close()


    @staticmethod
    def decrement_borrows(id) -> int:
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT total_borrows FROM members WHERE id = %s", (id,))
            set_borrows = cursor.fetchone()['total_borrows'] - 1
            if set_borrows < 0:
                set_borrows = 0
            logger.info(f"incrising member borrows ({set_borrows + 1} -> {set_borrows})")
            cursor.execute("UPDATE members SET total_borrows = %s WHERE id = %s", (set_borrows, id))
            conn.commit()
            logger.info("member update")
            return set_borrows
        finally:
            if conn:
                cursor.close()
                conn.close()


        
    
    @staticmethod
    def count_active_members() -> int:
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("looking into members")
            cursor.execute("SELECT COUNT(*) FROM members WHERE is_active = true")
            logger.info("summarizes")
            return cursor.fetchall()[0][0]
        finally:
            if conn:
                cursor.close()
                conn.close()
    

    @staticmethod
    def get_top_member() -> list[dict]:
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM members WHERE total_borrows != 0")
            members = cursor.fetchall()
            maximum = None
            for m in members:
                if maximum == None or m["total_borrows"] > maximum:
                    maximum = m["total_borrows"]
            output = []
            for m in members:
                if m["total_borrows"] == maximum:
                    output.append(m)
            return output
        finally:
            if conn:
                cursor.close()
                conn.close()
    
