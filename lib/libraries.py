from typing import LiteralString, final
from pymysql import connect
from pymysql.cursors import Cursor
import sys
from dotenv import load_dotenv
import os
from tabulate import tabulate

_ = load_dotenv()

db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASS", "")
db_database = os.getenv("DB_DATABASE", "passwords")

@final
class SqlServer:
    def __init__(self) -> None:
        try:
            self.conn = connect(
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
                     website varchar(255),
                     comment varchar(255)
                     );
        """

        _ = self.curr.execute(query=sql_init)
        self.conn.commit()

    def insert(self, username : str, password : str, website : str, comment : str) -> None:

        if comment == '':
            sql = """
            INSERT INTO passwords 
            VALUES (NULL, %s, %s, %s);
            """
            _ = self.curr.execute(sql, (username, password, website))
        else:
            sql = """
            INSERT INTO passwords 
            VALUES (NULL, %s, %s, %s, %s);
            """
            _ = self.curr.execute(sql, (username, password, website, comment))

        self.conn.commit()

    def delete(self, ID : int):
        sql = "DELETE FROM passwords WHERE id = %s"

        _ = self.curr.execute(sql, (ID,))

        self.conn.commit()
        print(f"Deleted {self.curr.rowcount} row(s).")

    def edit(self, id : int, username = None,
        password = None,
        website = None,
        comment = None):

        edits = """
        UPDATE passwords
            SET username = %s, password = %s, website = %s, comment = %s
            WHERE id = %s;
        """

        sql =  """ SELECT *
            FROM passwords
            WHERE id=%s;
            """

        _ = self.curr.execute(sql, (id,))

        results = self.curr.fetchone()
        print(type(results))

        if results == "None":
            print("no such id.. try again")
            return

        

        default_user = results[1]  # pyright: ignore[reportOptionalSubscript]
        default_password = results[2]  # pyright: ignore[reportOptionalSubscript]
        default_website = results[3]  # pyright: ignore[reportOptionalSubscript]
        default_comment = results[4]  # pyright: ignore[reportOptionalSubscript]

        if username is None or username == '':
            username = default_user
        if password is None or password == '':
            password = default_password
        if website is None or website == '':
            website = default_website
        if comment is None or comment == '':
            comment = default_comment 

        try:
            print("\nedited..")
            _ = self.curr.execute(edits, (username, password, website, comment, id))
            self.conn.commit()
            self.results(username, password, website)  # pyright: ignore[reportArgumentType]
        except Exception:
            print("error...")


    def search(self, search : str):
        sql =  f""" SELECT *
            FROM passwords
            WHERE website LIKE %s;
            """

        _ = self.curr.execute(query=sql, args=(f"%{search}%",))

        results = self.curr.fetchall()

        print(tabulate(results, headers=["ID", "username", "password", "website", "comment"], tablefmt="psql"))

        return results

    def results(self, username : str, password : str, website : str):
            sql =  """ SELECT *
            FROM passwords
            WHERE username=%s and website=%s and password=%s;
            """

            _ = self.curr.execute(query=sql, args=(username, website, password))

            results = self.curr.fetchall()

            print("\njob Results:")
            print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))

    def showall(self):
        sql: LiteralString =  f""" SELECT *
            FROM passwords
            """

        _ = self.curr.execute(query=sql)

        results = self.curr.fetchall()

        print(tabulate(tabular_data=results, headers=["ID", "username", "password", "website", "comment"], tablefmt="psql"))
        return results
