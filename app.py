import os
import random
import psycopg2
import psycopg2.pool
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")  

app = Flask(__name__)
app.secret_key = SECRET_KEY


db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL, sslmode="require")

def get_db_connection():
    return db_pool.getconn()

def release_db_connection(conn):
    db_pool.putconn(conn)

def generate_clip_id():
    return str(random.randint(1000, 9999))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_page():
    return render_template("get.html")

@app.route("/fun")
def fun():
    return render_template("fun.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/save", methods=["POST"])
def save_clipboard():
    data = request.json
    content = data.get("content")

    if not content:
        return jsonify({"success": False, "message": "Content cannot be empty"}), 400

    clip_id = generate_clip_id()

    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO clipboard (clip_id, content) VALUES (%s, %s)", (clip_id, content))
            conn.commit()
        return jsonify({"success": True, "clip_id": clip_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/get/<clip_id>", methods=["GET"])
def get_clipboard(clip_id):
    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT content FROM clipboard WHERE clip_id = %s", (clip_id,))
            result = cur.fetchone()

            if not result:
                return jsonify({"success": False, "message": "Not found"}), 404

        return jsonify({"success": True, "content": result[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        data = request.get_json()
        if data.get("username", "").lower() == ADMIN_USERNAME.lower() and data.get("password") == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return jsonify({"success": True})
        return jsonify({"success": False}), 401

    return render_template("admin.html")

# Fetch Data with Sorting
@app.route("/admin/data", methods=["GET"])
def fetch_data():
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 401

    order_by = "ASC" if request.args.get("sort") == "asc" else "DESC"

    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(f"SELECT * FROM clipboard ORDER BY created_at {order_by}")
            rows = cur.fetchall()

        return jsonify([
            {"id": row[0], "clip_id": row[1], "content": row[2], "created_at": row[3].strftime("%Y-%m-%d %H:%M:%S")}
            for row in rows
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete All Data
@app.route("/admin/delete", methods=["DELETE"])
def delete_all_data():
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM clipboard")
            conn.commit()
        return jsonify({"message": "All clipboard data deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0")
