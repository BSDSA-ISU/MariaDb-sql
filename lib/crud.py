import os
from dotenv import load_dotenv
import pymysql

_ = load_dotenv()

db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASS", "")
db_database = os.getenv("DB_DATABASE", "passwords")

def connect_db():
    return pymysql.connect(
        host="localhost",
        user=db_user,
        password=db_password,
        database=db_database,
        cursorclass=pymysql.cursors.Cursor,
        autocommit=False
    )