import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Connect to the database
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


# Query the database
def db_query(sql):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# Insert into the database
def db_insert(sql):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    lastrowid = cursor.lastrowid
    conn.commit()
    return lastrowid


# Delete from the database1
def db_delete(sql):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


# Update the database
def db_update(sql):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
