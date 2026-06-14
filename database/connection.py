import mysql.connector

def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost"
            port=3306
            user='root'
            password='secret'
            database='library_db'
        )
    



