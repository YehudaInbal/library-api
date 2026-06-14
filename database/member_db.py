from logger import get_logger
from database.connection_db import get_connection
from mysql.connector.errors import IntegrityError

logger = get_logger(__name__)


MEMBER_VALUES = ("is_active", "email", "name")


class Members:

    
    @staticmethod
    def add_member(data: dict) -> int:
        if "is_active" not in data:
            data["is_active"] = True
        try:
            conn = get_connection()
            cursor = conn.cursor()
            logger.info("starting to insert a member")
            cursor.execute("""INSERT INTO members(is_active, email, name)
            VALUES (%(is_active)s, %(email)s, %(name)s)""", data)
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
    def count_active_borrows_by_member(member_id) -> int:
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT total_borrows FROM members WHERE id = %s", (member_id,))
            return cursor.fetchone()['total_borrows']
        finally:
            if conn:
                cursor.close()
                conn.close()