from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "my_very_secret_key_123456789"  # Needed for sessions


# Initialize the database
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stddb (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM stddb")
    count = cursor.fetchone()[0]
    if count == 0:  # Insert sample users
        cursor.execute("INSERT INTO stddb (username, password) VALUES (?, ?)", ("admin", "1234"))
        cursor.execute("INSERT INTO stddb (username, password) VALUES (?, ?)", ("tabraiz", "pass123"))
        conn.commit()
    conn.close()


# Login Page
@app.route("/", methods=["GET", "POST"])
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
            return redirect(url_for("dashboard"))  # Redirect to dashboard after login
        else:
            message = "❌ Invalid username or password."

    return render_template("Welcome.html", message=message)


# Dashboard Page
@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for("login"))
    
    username = session['username']
    return render_template("Dashboard.html", username=username)


# Extra Pages
@app.route("/calender")
def calender():
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template("Calender.html")


@app.route("/career")
def career():
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template("Career.html")


@app.route("/progress")
def progress():
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template("Progress.html")


@app.route("/notes")
def notes():
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template("Notes.html")


@app.route("/chatbot")
def chatbot():
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template("Chatbot.html")


@app.route("/links")
def links():
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template("Links.html")


@app.route("/profile")
def profile():
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template("Profile.html")


# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)