import sys
import pymysql
from dotenv import load_dotenv
import os
from tabulate import tabulate

_ = load_dotenv()

db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASS", "")
db_database = os.getenv("DB_DATABASE", "passwords")

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

_ = curr.execute(sql_init)

conn.commit()

def insert(username : str, password : str, website : str) -> None:
    sql = """
        INSERT INTO passwords 
        VALUES (NULL, %s, %s, %s);
     """
    
    _ = curr.execute(sql, (username, password, website))

    conn.commit()

def delete(ID : int):
    sql = "DELETE FROM passwords WHERE id = %s"
    
    _ = curr.execute(sql, (ID,))

    conn.commit()
    print(f"Deleted {curr.rowcount} row(s).")

def edit(id : int, username: str | None = None ,
    password : str | None = None,
    website : str | None = None):

    edits = """
    UPDATE passwords
        SET username = %s, password = %s, website = %s
        WHERE id = %s;
    """
        
    sql =  """ SELECT *
        FROM passwords
        WHERE id=%s;
        """
    
    _ = curr.execute(sql, (id,))
    
    results = str(curr.fetchone())

    if results == "None":
        print("no such id.. try again")
        return

    default_user = str(results[1])
    default_password = str(results[2])
    default_website = str(results[3])

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
        conn.commit()
        print("\nedited..")
        _ = curr.execute(edits, (username, password, website, id))
    except Exception:
        print("error...")


def search(search : str):
    sql =  f""" SELECT *
        FROM passwords
        WHERE website LIKE %s;
        """
    
    _ = curr.execute(sql, (f"%{search}%",))
    
    results = curr.fetchall()

    print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))

def results(username : str, password : str, website : str):
        sql =  """ SELECT *
        FROM passwords
        WHERE username=%s and website=%s and password=%s;
        """

        _ = curr.execute(sql, (username, website, password))

        results = curr.fetchall()

        print("\njob Results:")
        print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))


def showall():
    sql =  f""" SELECT *
        FROM passwords
        """
    
    _ = curr.execute(sql)
    
    results = curr.fetchall()

    print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))

if __name__ == "__main__":
    edit(1, username="MyUsername", password="mypasswd")
