from flask import Flask, render_template, request, redirect, flash
import pymysql
from dotenv import load_dotenv
from lib.libraries import SqlServer

sql = SqlServer()

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True,port=42069)