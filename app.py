from flask import Flask, render_template, redirect, session, url_for, request
import sqlite3 as sql
from hashlib import sha256

conn = sql.connect('database.db')


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    hasha = sha256(password.encode())
    password = hasha.hexdigest()

    with sql.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * from login WHERE username = (?)", (username,))
        userd = c.fetchone()
        user = userd[0]
        pwd = userd[1]
    if username == user:
        if password == pwd:
            return render_template("logged.html")
        else:
            return redirect("/")
    else:
        return redirect("/")


@app.route("/create")
def create():
    return render_template("create-acc.html")

@app.route("/new-acc", methods=["GET", "POST"])
def newacc():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            hasha = sha256(password.encode())
            password = hasha.hexdigest()
            with sql.connect("database.db") as conn:
                c = conn.cursor()
                c.execute("INSERT INTO login (username, password) VALUES(?,?)", (username, password))
                conn.commit()
            return redirect("/")

        except:
            conn.rollback()
            return "Failed to create account"
    else:
        return "Please Log in"

if __name__ == '__main__':
    app.run(debug=True)