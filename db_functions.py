import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import mysql.connector


def get_db_connection():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        autocommit=True
    )
    return conn


def db_query(sql):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
