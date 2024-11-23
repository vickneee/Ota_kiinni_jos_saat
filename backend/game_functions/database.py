import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3306
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")

    # Connect to the database
    def get_db_connection(self):
        conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
            autocommit=True
        )
        return conn

    # Query the database
    def db_query(self,sql):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # Insert into the database
    def db_insert(self,sql):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        lastrowid = cursor.lastrowid
        conn.commit()
        return lastrowid

    # Delete from the database
    def db_delete(self,sql):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    # Update the database
    def db_update(self,sql):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
