import os
from typing import LiteralString
from dotenv import load_dotenv
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash


_ = load_dotenv()

db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASS", "")
db_database = os.getenv("DB_DATABASE", "passwords")

def connect_db():
    return pymysql.connect(
        host="localhost",
        user=db_user,
        password=db_password,
        database=db_database,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )

def showall(id):
    conn = connect_db()
    cur = conn.cursor()
    sql: LiteralString =  """ SELECT *
        FROM password_entries
        where user_id = %s
        """

    _ = cur.execute(sql, (id))
    results = cur.fetchall()
    return results


def edit(id: int, username=None, password=None,
    website=None, comment=None):
    conn = connect_db()
    curr = conn.cursor()

    sql = """ 
        SELECT username, password, website, comment 
        FROM password_entries
        WHERE id = %s;
    """
    curr.execute(sql, (id,))
    results = curr.fetchone()

    # FIX: Database drivers return Python None object, not "None" string
    if results is None:
        return False, "No such ID found."

    # Assign existing values if the new ones are missing or empty strings
    username = username.strip() if username and username.strip() else results.username
    password = password.strip() if password and password.strip() else results.password
    website = website.strip() if website and website.strip() else results.website
    comment = comment.strip() if comment and comment.strip() else results.comment

    edits = """
        UPDATE password_entries
        SET username = %s, password = %s, website = %s, comment = %s
        WHERE id = %s;
    """

    try:
        curr.execute(edits, (username, password, website, comment, id))
        conn.commit()
        
        # If your class has a self.results() method, you can still call it here:
        # self.results(username, password, website) 
        
        return True, "Successfully updated."
    except Exception as e:
        conn.rollback()
        return False, f"Database error: {str(e)}"
    finally:
        curr.close()
        conn.close()

def add(id: int, username=None, password=None,
    website=None, comment=None):
    conn = connect_db()
    curr = conn.cursor()

    sql = """ 
        INSERT INTO password_entries (user_id, username, password, website, comment)
        VALUES (%s, %s, %s, %s, %s);
    """
    try:
        curr.execute(sql, (id, username, password, website, comment))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False, f"Database error: {str(e)}"
    finally:
        curr.close()
        conn.close()

if __name__ == "__main__":
    print(showall(1))