import os
import sqlite3

def is_strong_password(password):
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    return True

from flask import Flask, render_template, request, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)

csrf = CSRFProtect(app)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "Welcome to Secure Login System"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not is_strong_password(password):
            return "Password must be at least 8 characters long and contain uppercase, lowercase, and a number"

        password_hash = generate_password_hash(password)

        conn = get_db_connection()

        try:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists"

        conn.close()

        return "Registration successful"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["username"] = user["username"]
            return "Login successful"

        return "Invalid username or password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return "Please login first"

    return f"Welcome, {session['username']}!"

@app.route("/logout")
def logout():
    session.pop("username", None)
    return "Logged out successfully"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
