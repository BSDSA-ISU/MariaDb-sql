# Insertion and entering
import sys
import mariadb
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_database = os.getenv("DB_DATABASE")

try:
    conn = mariadb.connect(
        user=db_user,
        password=db_password,
        host="localhost",
        database=db_database
    )
except Exception:
    print("you suck! run mariadb server!")
    sys.exit(1)

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

def search(search):
    sql =  f""" SELECT *
        FROM passwords
        WHERE website LIKE %s;
        """
    
    curr.execute(sql, (f"%{search}%",))
    
    results = curr.fetchall()

    for row in results:
        print(row)
