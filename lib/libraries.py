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

sql_init = """
             CREATE TABLE IF NOT EXISTS passwords (
             id INT AUTO_INCREMENT PRIMARY KEY,
             username varchar(255),
             password varchar(255),
             website varchar(255)
             );
"""

curr.execute(sql_init)

conn.commit()

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

def edit(id : int, username = None, password = None, website = None):

    edits = """
    UPDATE passwords
        SET username = %s, password = %s, website = %s
        WHERE id = %s;
    """
        
    sql =  """ SELECT *
        FROM passwords
        WHERE id=%s;
        """
    
    curr.execute(sql, (id,))
    
    results = curr.fetchone()

    if results is None:
        print("no such id.. try again")
        return

    default_user = results[1]
    default_password = results[2]
    default_website = results[3]

    if username is None:
        username = default_user
    if password is None:
        password = default_password
    if website is None:
        website = default_website   

    if username is default_user and password is default_password and website is default_website:
        username = input("Insert new username(Leave blank for default)\n>>")
        if username == "":
            username = default_user

        password = input("Insert new username(leave blank for default)\n>>")
        if password == "":
            password = default_password

        website = input("Insert new username(leave blank for default)\n>>")
        if website == "":
            website = default_website
    
    try:
        curr.execute(edits, (username, password, website, id))
        conn.commit()
        print("edited..")
    except Exception:
        print("error...")


def search(search):
    sql =  f""" SELECT *
        FROM passwords
        WHERE website LIKE %s;
        """
    
    curr.execute(sql, (f"%{search}%",))
    
    results = curr.fetchall()

    print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))

def results(username, password, website):
        sql =  """ SELECT *
        FROM passwords
        WHERE username=%s and website=%s and password=%s;
        """

        curr.execute(sql, (username, website, password))

        results = curr.fetchall()

        print("\njob Results:")
        print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))


def showall():
    sql =  f""" SELECT *
        FROM passwords
        """
    
    curr.execute(sql)
    
    results = curr.fetchall()

    print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))

if __name__ == "__main__":
    edit(1, username="MyUsername", password="mypasswd")
