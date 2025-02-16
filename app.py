import os
import random
import psycopg2
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import threading
import time

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

def generate_clip_id():
    return str(random.randint(1000, 9999))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_page():
    return render_template("get.html")

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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO clipboard (clip_id, content) VALUES (%s, %s)", (clip_id, content))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"success": True, "clip_id": clip_id})

@app.route("/get/<clip_id>", methods=["GET"])
def get_clipboard(clip_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT content FROM clipboard WHERE clip_id = %s", (clip_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({"success": True, "content": result[0]}) if result else jsonify({"success": False, "message": "Not found"}), 404

@app.route("/fun")
def fun_page():
    return render_template("fun.html")


if __name__ == "__main__":
    app.run(debug=True)
