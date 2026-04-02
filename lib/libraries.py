# Insertion and entering
import sys
import pymysql
from dotenv import load_dotenv
import os
from tabulate import tabulate

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_database = os.getenv("DB_DATABASE")

try:
    conn = pymysql.connect(
        user=db_user,
        password=db_password,
        host="localhost",
        database=db_database
    )
except Exception:
    print("you suck! run mariadb or mysql server!")
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

    print(tabulate(results, headers=["username", "password", "website"], tablefmt="psql"))

if __name__ == "__main__":
    search("a")
