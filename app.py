from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "cheetah"


# ---------------- DATABASE INIT ----------------

def init_db():

    conn = sqlite3.connect("database/users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("database/users.db")
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO users(username,password) VALUES (?,?)",
        (username,hashed_password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/users.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect("/dashboard")

        else:
            return "Invalid username or password"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])


# ---------------- INTERVIEW ----------------

@app.route("/interview")
def interview():
    return render_template("interview.html")


# ---------------- DAILY ----------------

@app.route("/daily")
def daily():

    challenge = "Explain Object Oriented Programming."

    return render_template("daily.html", challenge=challenge)


# ---------------- LEADERBOARD ----------------

@app.route("/leaderboard")
def leaderboard():

    conn = sqlite3.connect("database/leaderboard.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores(
    name TEXT,
    score INTEGER
    )
    """)

    data = cur.execute(
    "SELECT * FROM scores ORDER BY score DESC"
    ).fetchall()

    conn.close()

    return render_template("leaderboard.html", data=data)


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("user",None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)