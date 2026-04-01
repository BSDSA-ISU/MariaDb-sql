import mariadb

conn = mariadb.connect(
    user="ali",
    password="toshinoukyouko",
    host="localhost",
    database="password"
)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            password VARCHAR(255),
            website VARCHAR(255)
            )""")

# INSERT INTO passwords 
# VALUES (NULL, 'jdoe', 'p@ssword123', 'github.com');

# INSERT INTO Users (first_name, last_name, email)
# VALUES ('Alice', 'Smith', 'alice@example.com');

conn.commit()

cur.execute("SELECT * FROM passwords;")
for row in cur:
    print(row)
