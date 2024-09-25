import os
from dotenv import load_dotenv
load_dotenv()

import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
    host='localhost',
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    )
    return conn
