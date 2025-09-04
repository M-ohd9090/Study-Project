from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ----------------- DB HELPER -----------------
def get_db():
    conn = sqlite3.connect("mtdatabase.db")
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            steps INTEGER NOT NULL,
            completed_steps INTEGER DEFAULT 0,
            start_date TEXT,
            end_date TEXT,
            category TEXT,
            note TEXT,
            reminder_time TEXT,
            status TEXT DEFAULT 'active'
        )
    """)
    conn.commit()
    conn.close()

# ----------------- ROUTES -----------------

@app.route("/")
def index():
    # renders your HTML file
    return render_template("Progress.html")

# Add new goal
@app.route("/add_goal", methods=["POST"])
def add_goal():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO goals (title, steps, start_date, end_date, category, note, reminder_time, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["title"], data["steps"], data.get("start_date"), data.get("end_date"),
        data.get("category"), data.get("note"), data.get("reminder_time"), "active"
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Goal added successfully!"})

# Get all goals (with expiry auto-check)
@app.route("/get_goals")
def get_goals():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals")
    rows = cursor.fetchall()
    goals = []

    today = datetime.today().date()

    for row in rows:
        status = row["status"]

        # Expiry check
        if row["end_date"]:
            end_date = datetime.strptime(row["end_date"], "%Y-%m-%d").date()
            if today > end_date and status != "completed":
                status = "expired"
                cursor.execute("UPDATE goals SET status = ? WHERE id = ?", ("expired", row["id"]))
                conn.commit()

        goals.append({
            "id": row["id"],
            "title": row["title"],
            "steps": row["steps"],
            "completed_steps": row["completed_steps"],
            "start_date": row["start_date"],
            "end_date": row["end_date"],
            "category": row["category"],
            "note": row["note"],
            "reminder_time": row["reminder_time"],
            "status": status
        })

    conn.close()
    return jsonify(goals)

# Update progress
@app.route("/update_progress/<int:goal_id>", methods=["POST"])
def update_progress(goal_id):
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE goals
        SET completed_steps = ?,
            status = ?
        WHERE id = ?
    """, (data["completed_steps"], data["status"], goal_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Progress updated!"})

# Delete goal
@app.route("/delete_goal/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Goal deleted successfully!"})

# ----------------- RUN APP -----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=0)  # dynamic port