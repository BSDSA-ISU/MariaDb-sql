from flask import Flask, render_template, request, redirect, flash
import pymysql
from dotenv import load_dotenv
from lib.libraries_flask import SqlServer
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

@app.route("/", methods=["GET", "POST"])
def index():
    dar = sql.showall()
    return render_template("index.html", hello="powered by Koishi Vibes", lists=dar)

@app.route("/search")
def search_accounts():
    query = request.args.get('q', '')
    # Assuming 'db' is your database object instance
    results = sql.search(query) 
    return render_template("parts/account_list.html", lists=results)

@app.route("/add", methods=["GET", "POST"])
def add_account():
    return "0"

def open_browser():
    webbrowser.open("http://127.0.0.1:42069")

#Timer(1, open_browser).start()

if __name__ == "__main__":
    app.run(debug=True,port=42069)