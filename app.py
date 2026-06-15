import os
from flask import Flask, render_template, request, redirect, flash, url_for
from dotenv import load_dotenv
from lib.libraries_flask import SqlServer
from lib import crud
import webbrowser
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from lib.connector import connect_db
from werkzeug.security import check_password_hash
from cryptography.fernet import Fernet

# 1. Load the environment variables from the .env file
load_dotenv()

# 2. Grab the key from the environment
encryption_key_string = os.getenv("ENCRYPTION_KEY")

if not encryption_key_string:
    raise ValueError("No ENCRYPTION_KEY found in environment variables!")

# 3. Fernet expects bytes, so encode the string version
ENCRYPTION_KEY = encryption_key_string.encode()
cipher = Fernet(ENCRYPTION_KEY)


sql = SqlServer()

app = Flask(__name__)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
# Redirects users to the 'login' route if they try to access a protected page
login_manager.login_view = 'login'  # pyright: ignore[reportAttributeAccessIssue]
app.secret_key = 'Koishi-Komeiji'

# user loader
class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name

# login session user
@login_manager.user_loader
def load_user(user_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, password_hash
        FROM users
        WHERE id = %s
    """, (user_id,))
    
    user_data = cur.fetchone()
    conn.close()
    if user_data:
        # Assuming your User class accepts these parameters
        # You can now also pass 'name' if you want it available in current_user
        return User(user_data[0], user_data[1])
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        cur = conn.cursor()

        # Check credentials in the athletes table
        cur.execute("""
            SELECT id, username, password_hash
            FROM users
            WHERE username = %s
        """, (username,))
        
        user_data = cur.fetchone()
        conn.close()

        if user_data and check_password_hash(user_data[2], password):
            user_obj = User(
                user_data[0],
                user_data[1],
            )

            login_user(user_obj)
            return redirect("/")

        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")

# logout
@app.route('/logout')
@login_required # Prevents users who aren't logged in from hitting this route
def logout():
    # This deletes the session cookie and clears current_user
    logout_user() 
    
    flash('You have been logged out.')
    return redirect(url_for('login'))

# root or index
@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        dar = crud.showall(current_user.id)
        for items in dar:

            try:
                x = items['password']
                raw_password  = cipher.decrypt(x.encode()).decode()
                items['password'] = raw_password
            except Exception as e:
                print(e)
                pass

        print(dar)
        return render_template("index.html", hello="powered by Koishi Vibes", lists=dar)
        
    else:
        return redirect(url_for("login"))

@app.route("/search")
def search_accounts():
    query = request.args.get('q', '')
    # Assuming 'db' is your database object instance
    results = sql.search(query)
    
    return render_template("parts/account_list.html", lists=results)

@app.route("/add/<int:id>", methods=["GET", "POST"])
@login_required
def add_account(id):
    user_id = current_user.id
    if request.method == "POST":
        username = request.form.get("username")
        raw_password = request.form.get("password")  # The plain text password
        website = request.form.get("website")
        comment = request.form.get("comment")

        # 🔒 ENCRYPT IT BEFORE SAVING
        # Fernet requires bytes, so we encode the string, encrypt it, then decode back to a string for the DB
        encrypted_password = cipher.encrypt(raw_password.encode()).decode()

        if not comment:
            comment = None

        x = crud.add(
            id=user_id,
            username=username,
            password=encrypted_password, # 👈 Save the encrypted string instead!
            website=website,
            comment=comment
        )

        if x:
            return redirect("/")

    return render_template("add.html", id=id)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_password(id):
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        # ... (Keep your security check code the same) ...

        username = request.form.get("username")
        raw_password = request.form.get("password")
        website = request.form.get("website")
        comment = request.form.get("comment")

        # 🔒 ENCRYPT IT BEFORE UPDATING
        encrypted_password = cipher.encrypt(raw_password.encode()).decode()

        success, message = crud.edit(
            id=id,
            username=username,
            password=encrypted_password, # 👈 Update with encrypted version
            website=website,
            comment=comment
        )
        conn.close()

        if success:
            return redirect("/")
        
        # ... (Handle failure state) ...

    # --- GET REQUEST (Displaying the form) ---
    sql = "SELECT username, password, website, comment, user_id FROM password_entries WHERE id = %s;"
    cur.execute(sql, (id,))
    result = cur.fetchone()
    conn.close()

    if not result:
        return "No such entry found.", 404

    db_user_id = result[4]
    if db_user_id != int(current_user.id):
        return "Access Denied", 403

    # 🔓 DECRYPT IT SO THE USER CAN SEE IT
    encrypted_db_password = result[1]
    try:
        decrypted_password = cipher.decrypt(encrypted_db_password.encode()).decode()
    except Exception:
        decrypted_password = "Error decrypting password" # Safeguard if data gets corrupted

    entry = {
        "username": result[0],
        "password": decrypted_password, # 👈 Pass plain text back to the HTML form
        "website": result[2],
        "comment": result[3]
    }

    return render_template("edit.html", entry=entry)

def open_browser():
    webbrowser.open("http://127.0.0.1:42069")



#Timer(1, open_browser).start()

"""
if __name__ == "__main__":
    from waitress import serve
    print("Serving on port 42069...")
    serve(app, host="0.0.0.0", port=42069)


"""
if __name__ == "__main__":
    app.run(debug=True,port=42069)


