import sqlite3
import pymysql
import os
import dotenv

dotenv.load_dotenv()

db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASS", "")
db_database = os.getenv("DB_DATABASE", "passwords")

def migrate() -> None:
    # --- Connect to SQLite ---
    sqlite_conn = sqlite3.connect('./localserver/passwords.db')
    sqlite_cursor = sqlite_conn.cursor()

    # --- Connect to MariaDB ---
    mariadb_conn = pymysql.connect(
        host='localhost',
        user=db_user,
        password=db_password,
        database=db_database
    )
    mariadb_cursor = mariadb_conn.cursor()

    # --- Read data from SQLite ---
    sqlite_cursor.execute("SELECT * FROM passwords")
    rows = sqlite_cursor.fetchall()

    # --- Insert into MariaDB ---
    for row in rows:
        # Assuming your_table has same columns and same order
        placeholders = ', '.join(['%s'] * len(row))
        sql = f"INSERT INTO passwords VALUES ({placeholders})"
        mariadb_cursor.execute(sql, row)

    mariadb_conn.commit()

    # --- Close connections ---
    sqlite_conn.close()
    mariadb_conn.close()

    print("Migration done! 🚀")


if __name__ == "__main__":
    migrate()