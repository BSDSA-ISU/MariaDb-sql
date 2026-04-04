from sqlite3 import Connection, Cursor, connect
from typing import LiteralString
from tabulate import tabulate

class local:
    def __init__(self) -> None:
        self.conn: Connection = connect(database="./localserver/passwords.db")

        self.curr: Cursor = self.conn.cursor()

        sql_init = """
                     CREATE TABLE IF NOT EXISTS passwords (
                     id INTEGER PRIMARY KEY,
                     username varchar(255),
                     password varchar(255),
                     website varchar(255)
                     );
        """

        _ = self.curr.execute(sql_init)
        self.conn.commit()

    def insert(self, username : str, password : str, website : str) -> None:
        sql = """
            INSERT INTO passwords 
            VALUES (NULL, ?, ?, ?);
         """

        _ = self.curr.execute(sql, (username, password, website))

        self.conn.commit()

    def delete(self, ID : int):
        sql = "DELETE FROM passwords WHERE id = ?"

        _ = self.curr.execute(sql, (ID,))

        self.conn.commit()
        print(f"Deleted {self.curr.rowcount} row(s).")

    def edit(self, id : int, username: str | None = None ,
        password : str | None = None,
        website : str | None = None):

        edits = """
        UPDATE passwords
            SET username = ?, password = ?, website = ?
            WHERE id = ?;
        """

        sql =  """ SELECT *
            FROM passwords
            WHERE id=?;
            """

        _ = self.curr.execute(sql, (id,))

        results = str(self.curr.fetchone())  # pyright: ignore[reportAny]

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
            WHERE website LIKE ?;
            """

        _ = self.curr.execute(sql, (f"%{search}%",))

        results = self.curr.fetchall()

        print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))

    def results(self, username : str, password : str, website : str):
            sql =  """ SELECT *
            FROM passwords
            WHERE username=? and website=? and password=?;
            """

            _ = self.curr.execute(sql, (username, website, password))

            results = self.curr.fetchall()

            print("\njob Results:")
            print(tabulate(results, headers=["ID", "username", "password", "website"], tablefmt="psql"))

    def showall(self) -> None:
        sql: LiteralString =  f""" SELECT *
            FROM passwords
            """

        _ = self.curr.execute(sql)

        results = self.curr.fetchall()

        print(tabulate(tabular_data=results, headers=["ID", "username", "password", "website"], tablefmt="psql"))

if __name__ == "__main__":
    x: local = local()
    x.insert("x", "y", "z")
    x.showall()