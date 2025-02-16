import os
import random
import psycopg2
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from datetime import datetime, timedelta
import threading
import time

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:online-clipboard@aws-0-ap-south-1.pooler.supabase.com:6543/postgres")

app = Flask(__name__)

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

# Generate a random 4-digit ID
def generate_clip_id():
    return str(random.randint(1000, 9999))

# Route: Home Page (Paste & Save)
@app.route("/")
def index():
    return render_template("index.html")

# Route: Retrieve Page
@app.route("/get")
def get_page():
    return render_template("get.html")

# API: Save Clipboard Data
@app.route("/save", methods=["POST"])
def save_clipboard():
    try:
        data = request.json
        content = data.get("content")

        if not content:
            return jsonify({"success": False, "message": "Content cannot be empty"}), 400

        clip_id = generate_clip_id()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO clipboard (clip_id, content) VALUES (%s, %s) RETURNING clip_id", (clip_id, content))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"success": True, "clip_id": clip_id})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# API: Retrieve Clipboard Data
@app.route("/get/<clip_id>", methods=["GET"])
def get_clipboard(clip_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT content FROM clipboard WHERE clip_id = %s", (clip_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return jsonify({"success": True, "content": result[0]})
        else:
            return jsonify({"success": False, "message": "Clipboard content not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Function to clear old clipboard data every 2 hours
def clear_old_data():
    while True:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM clipboard WHERE created_at < NOW() - INTERVAL '2 hours'")
            conn.commit()
            cur.close()
            conn.close()
            print("🧹 Old clipboard data cleared")
        except Exception as e:
            print(f"❌ Error clearing old data: {e}")
        
        time.sleep(2 * 60 * 60)  # Run every 2 hours

# Start cleanup thread
threading.Thread(target=clear_old_data, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)
