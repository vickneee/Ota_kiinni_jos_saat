import os
from dotenv import load_dotenv
load_dotenv()


import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    autocommit=True
    )
    return conn

def db_query(sql):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


