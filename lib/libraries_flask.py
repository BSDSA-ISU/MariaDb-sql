from typing import LiteralString, final
from pymysql import connect
from pymysql.cursors import Cursor
import sys
from dotenv import load_dotenv
import os
from tabulate import tabulate
from pymysql.cursors import DictCursor

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
                database=db_database,
                cursorclass=DictCursor
            )

        except Exception as e:
            print("you suck! run mariadb or mysql server!")
            print(e)
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

    def edit(self, id: int, username=None, password=None, website=None, comment=None):
        sql = """ 
            SELECT username, password, website, comment 
            FROM passwords 
            WHERE id = %s;
        """
        self.curr.execute(sql, (id,))
        results = self.curr.fetchone()

        # FIX: Database drivers return Python None object, not "None" string
        if results is None:
            return False, "No such ID found."

        # Assign existing values if the new ones are missing or empty strings
        username = username if username else results[0]
        password = password if password else results[1]
        website = website if website else results[2]
        comment = comment if comment else results[3]

        edits = """
            UPDATE passwords
            SET username = %s, password = %s, website = %s, comment = %s
            WHERE id = %s;
        """

        try:
            self.curr.execute(edits, (username, password, website, comment, id))
            self.conn.commit()
            
            # If your class has a self.results() method, you can still call it here:
            # self.results(username, password, website) 
            
            return True, "Successfully updated."
        except Exception as e:
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def search(self, search : str):
        sql =  """ SELECT *
            FROM password_entries
            WHERE website LIKE %s;
            """

        self.curr.execute(sql, (f"%{search}%",))

        results = self.curr.fetchall()

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
            FROM password_entries
            """

        _ = self.curr.execute(query=sql)

        results = self.curr.fetchall()
        return results

