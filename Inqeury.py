from flask import Flask, render_template, request
import sqlite3
import socket   # ✅ for finding free port

app = Flask(__name__)

# ✅ Create table if not exists
def init_db():
    conn = sqlite3.connect("mtdatabase.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Route to show your profile page (with About, Help, Contact form)
@app.route("/")
def home():
    return render_template("Profile.html")   # Keep your HTML inside templates/

# Route to handle form submission
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    conn = sqlite3.connect("mtdatabase.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_inquiries (name, email, message) VALUES (?, ?, ?)", 
                   (name, email, message))
    conn.commit()
    conn.close()

    return f"<h2>Thank you, {name}! Your inquiry has been submitted.</h2><a href='/profile'>Back</a>"

# ✅ Function to find free port
def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))  # Let OS assign a free port
    port = s.getsockname()[1]
    s.close()
    return port

if __name__ == "__main__":
    free_port = find_free_port()
    print(f"✅ Flask Inquiry Form running on port {free_port}")
    app.run(host="0.0.0.0", port=free_port, debug=True)