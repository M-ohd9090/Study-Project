from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import socket

app = Flask(__name__)
app.secret_key = "my_very_secret_key_123456789"  # Needed for sessions

# 🔹 Dynamic free port finder
def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port

# Initialize the database
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stddb (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# 🔹 Home route → redirects to signup
@app.route("/")
def home():
    return redirect(url_for("signup"))

# 🔹 Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirmPassword"]

        if password != confirm_password:
            message = "❌ Passwords do not match!"
        else:
            try:
                conn = sqlite3.connect("students.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO stddb (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                conn.close()
                message = "✅ Signup successful! Please login."
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                message = "⚠️ Username already exists. Try another."

    return render_template("Signup.html", message=message)

# 🔹 Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stddb WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for("dashboard"))
        else:
            message = "❌ Invalid username or password."

    return render_template("Welcome.html", message=message)

# 🔹 Dashboard
@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for("login"))
    return f"👋 Welcome, {session['username']}! This is your dashboard."

# 🔹 Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    free_port = get_free_port()
    print(f"🚀 Running on http://127.0.0.1:{free_port}")
    app.run(host="0.0.0.0", port=free_port, debug=True)
