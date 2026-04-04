from typing import LiteralString
from pymysql.cursors import Cursor


import sys
import pymysql
from dotenv import load_dotenv
import os
from tabulate import tabulate

_ = load_dotenv()

db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASS", "")
db_database = os.getenv("DB_DATABASE", "passwords")

class SqlServer:
    def __init__(self) -> None:
        try:
            self.conn = pymysql.connect(
                user=db_user,
                password=db_password,
                host="localhost",
                database=db_database
            )

        except Exception:
            print("you suck! run mariadb or mysql server!")
            sys.exit(1)

        self.curr: Cursor = self.conn.cursor()

        sql_init = """
                     CREATE TABLE IF NOT EXISTS passwords (
                     id INT AUTO_INCREMENT PRIMARY KEY,
                     username varchar(255),
                     password varchar(255),
                     website varchar(255)
                     );
        """

        _ = self.curr.execute(query=sql_init)
        self.conn.commit()

    def insert(self, username : str, password : str, website : str) -> None:
        sql = """
            INSERT INTO passwords 
            VALUES (NULL, %s, %s, %s);
         """

        _ = self.curr.execute(sql, (username, password, website))

        self.conn.commit()

    def delete(self, ID : int):
        sql = "DELETE FROM passwords WHERE id = %s"

        _ = self.curr.execute(sql, (ID,))

        self.conn.commit()
        print(f"Deleted {self.curr.rowcount} row(s).")

    def edit(self, id : int, username: str | None = None ,
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

        _ = self.curr.execute(sql, (id,))

        results = str(self.curr.fetchone())

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
            self.conn.commit()
            print("\nedited..")
            _ = self.curr.execute(edits, (username, password, website, id))
        except Exception:
            print("error...")


    def search(self, search : str) -> None:
        sql =  f""" SELECT *
            FROM passwords
            WHERE website LIKE %s;
            """

        _ = self.curr.execute(query=sql, args=(f"%{search}%",))

        results = self.curr.fetchall()

        print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))

    def results(self, username : str, password : str, website : str):
            sql =  """ SELECT *
            FROM passwords
            WHERE username=%s and website=%s and password=%s;
            """

            _ = self.curr.execute(query=sql, args=(username, website, password))

            results = self.curr.fetchall()

            print("\njob Results:")
            print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))

    def showall(self) -> None:
        sql: LiteralString =  f""" SELECT *
            FROM passwords
            """

        _ = self.curr.execute(query=sql)

        results = self.curr.fetchall()

        print(tabulate(tabular_data=results, headers=["ID", "username", "password", "website"], tablefmt="psql"))


