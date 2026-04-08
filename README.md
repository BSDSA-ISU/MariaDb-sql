# :lock: SQL password manager

- [:lock: SQL password manager](#lock-sql-password-manager)
  - [:apple: Simple password manager via Mysql and Mariadb server](#apple-simple-password-manager-via-mysql-and-mariadb-server)
  - [Installation](#installation)
    - [:window: :penguin: Windows and Linux: Using uv(recommended)](#window-penguin-windows-and-linux-using-uvrecommended)
    - [:penguin: Linux: using pip](#penguin-linux-using-pip)
    - [:window: Windows: using pip](#window-windows-using-pip)
  - [Running](#running)
    - [:window: :penguin: Windows and Linux: using uv(recommended)](#window-penguin-windows-and-linux-using-uvrecommended-1)
    - [:window: Windows: using python](#window-windows-using-python)
    - [:penguin: Linux: using python](#penguin-linux-using-python)
  - [:warning: Important: It is highly recommended that you set a user and password on your SQL/MariaDB server before running the manager](#warning-important-it-is-highly-recommended-that-you-set-a-user-and-password-on-your-sqlmariadb-server-before-running-the-manager)
    - [If your server is still not configured, follow these steps](#if-your-server-is-still-not-configured-follow-these-steps)
  - [:question: What if I'm using sqlite instead?](#question-what-if-im-using-sqlite-instead)
  - [:books: Additional Resources](#books-additional-resources)

## :apple: Simple password manager via Mysql and Mariadb server

[Demo](https://github.com/user-attachments/assets/16eff880-54aa-4df6-9879-e481799d9b8c)

---

## Installation

### :window: :penguin: Windows and Linux: Using [uv](https://github.com/astral-sh/uv)(recommended)

```bash
uv sync
```

### :penguin: Linux: using pip

```bash
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

### :window: Windows: using pip

```ps1
python -m venv .venv

.\.venv\Scripts\activate

pip install -r requirements.txt
```

## Running

### :window: :penguin: Windows and Linux: using uv(recommended)

```ps1
uv run main.py
```

### :window: Windows: using python

```ps1
# Activating
.\.venv\Scripts\activate

# Executing
python main.py
```

### :penguin: Linux: using python

```bash
# Activating the environment
source ./.venv/bin/activate

# Running
python main.py
```

You can sneak that in as a **warning/note right before users run the app**, so they see it before trying to connect to the SQL server. Here's a clean way to add it to your markdown:

## :warning: Important: It is highly recommended that you set a user and password on your SQL/MariaDB server before running the manager

### If your server is still not configured, follow these steps

1. **Log in as root** (the default admin user)

   On **Linux** / WSL / Mac:

   ```bash
   sudo mysql -u root
   ```

   On **Windows** (Command Prompt or PowerShell):

   ```ps1
   mysql -u root -p
   ```

2. **Run the secure installation wizard** (if first time):

   ```bash
   sudo mysql_secure_installation

3. Create a new user:

    ```sql
    CREATE USER 'youruser'@'localhost' IDENTIFIED BY 'yourpassword';
    ```

4. Grant privileges to the user:

    ```sql
    GRANT ALL PRIVILEGES ON yourdatabase.* TO 'youruser'@'localhost';
    FLUSH PRIVILEGES;
    ```

5. Update your `.env` file with the new user credentials:

    ```env
    DB_USER=youruser
    DB_PASS=yourpassword
    DB_SERVER="mysql or mariadb"
    ```

This way its:

- **Prominent** but not intrusive  
- Gives both the *recommendation* and *steps*  
- Keeps your markdown clean and readable

## :question: What if I'm using sqlite instead?

Then good for you, its already secured, just don't loose your key

---

## :books: Additional Resources

- [The Python programming language](https://www.python.org/)
  - [pymysql library documentation](https://pymysql.readthedocs.io/en/latest/)
- [Mariadb Resources](https://mariadb.org/)
- [xampp manager](https://www.apachefriends.org/)
- [Mysql Community Server](https://dev.mysql.com/downloads/mysql/8.0.html)

---

![Koishi](https://media1.tenor.com/m/200dytcMF54AAAAd/koishi-dance.gif)

> Love from koishi :green_heart:
