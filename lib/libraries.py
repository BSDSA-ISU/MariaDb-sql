# Insertion and entering
import mariadb
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_database = os.getenv("DB_DATABASE")

conn = mariadb.connect(
    user=db_user,
    password=db_password,
    host="localhost",
    database=db_database
)

curr = conn.cursor()

def insert(username, password, website):
    sql = """
        INSERT INTO passwords 
        VALUES (NULL, %s, %s, %s);
     """
    
    curr.execute(sql, (username, password, website))

    conn.commit()

def delete(ID : int):
    sql = "DELETE FROM passwords WHERE id = %s"
    curr.execute(sql, (ID,))

    conn.commit()
    print(f"Deleted {curr.rowcount} row(s).")

def edit():
    print("soon lol")

delete(9)