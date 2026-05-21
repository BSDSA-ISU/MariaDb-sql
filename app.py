from flask import Flask, render_template, request, redirect, flash, url_for
import pymysql
from dotenv import load_dotenv
from lib.libraries_flask import SqlServer
from lib import crud
import webbrowser
from threading import Timer
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from lib.connector import connect_db
from werkzeug.security import generate_password_hash, check_password_hash

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
        id = crud.fetch_id(current_user.id)
        return render_template("index.html", hello="powered by Koishi Vibes", lists=dar, id=id)
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
        password = request.form.get("password")
        website = request.form.get("website")
        comment = request.form.get("comment")

        if not comment:
            comment = None

        x = crud.add(
            id=user_id,
            username=username,
            password=password,
            website=website,
            comment=comment
        )

        if x:
            return redirect("/")

    return render_template("add.html", id=id)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required # 👈 1. Stop unauthenticated users entirely
def edit_password(id):
    conn = connect_db()
    cur = conn.cursor()

    # --- SECURITY CHECK FOR POST REQUESTS ---
    if request.method == "POST":
        # Double check ownership before updating, just in case they forge the POST request
        cur.execute("SELECT user_id FROM password_entries WHERE id = %s", (id,))
        owner = cur.fetchone()
        if not owner or owner[0] != int(current_user.id):
            conn.close()
            return "Unauthorized action.", 403

        username = request.form.get("username")
        password = request.form.get("password")
        website = request.form.get("website")
        comment = request.form.get("comment")

        success, message = crud.edit(
            id=id,
            username=username,
            password=password,
            website=website,
            comment=comment
        )
        conn.close()

        if success:
            return redirect("/")

        return render_template(
            "edit.html",
            message=message,
            entry={
                "username": username,
                "password": password,
                "website": website,
                "comment": comment
            }
        )

    # --- SECURITY CHECK FOR GET REQUESTS ---
    # Include user_id in the SELECT statement
    sql = """
        SELECT username, password, website, comment, user_id
        FROM password_entries
        WHERE id = %s;
    """

    cur.execute(sql, (id,))
    result = cur.fetchone()
    conn.close()

    if not result:
        return "No such entry found.", 404

    # 2. Verify Ownership: Does this entry belong to the logged-in user?
    db_user_id = result[4]
    if db_user_id != int(current_user.id):
        return "Access Denied: You do not own this entry.", 403 # 👈 Instantly blocks URL sniffers

    entry = {
        "username": result[0],
        "password": result[1],
        "website": result[2],
        "comment": result[3]
    }

    return render_template("edit.html", entry=entry)

def open_browser():
    webbrowser.open("http://127.0.0.1:42069")



#Timer(1, open_browser).start()

if __name__ == "__main__":
    app.run(debug=True,port=42069)