from flask import Flask, render_template
from flask import request, jsonify
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Fixed path to point to 'templates' folder instead of looking for a 'frontend' folder outside the directory
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

@app.route('/')
def home():
    return render_template('index.html')

# Fixed path to create the database in the current directory to avoid "folder not found" errors
DB_PATH = os.path.join(BASE_DIR, 'travelmate.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            distance REAL NOT NULL,
            fare REAL NOT NULL,
            search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    

# API endpoint to save search details
@app.route('/api/save_search', methods=['POST'])
def save_search():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No JSON data received"
        }), 400

    distance = data.get('distance')
    fare = data.get('fare')

    if distance is None or fare is None:
        return jsonify({
            "status": "error",
            "message": "Distance and fare are required"
        }), 400

    try:
        distance = float(distance)
        fare = float(fare)

        if distance < 0 or fare < 0:
            return jsonify({
                "status": "error",
                "message": "Distance and fare cannot be negative"
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "message": "Distance and fare must be valid numbers"
        }), 400

    conn = get_db_connection()

    try:
        conn.execute(
            """
            INSERT INTO search_history (distance, fare)
            VALUES (?, ?)
            """,
            (distance, fare)
        )
        conn.commit()

    except sqlite3.Error:
        return jsonify({
            "status": "error",
            "message": "Could not save search details"
        }), 500

    finally:
        conn.close()

    return jsonify({
        "status": "success",
        "message": "Search details saved successfully",
        "recorded_distance": distance,
        "recorded_fare": fare
    }), 200


# API endpoint to retrieve search history
@app.route('/api/search_history', methods=['GET'])
def search_history():
    conn = get_db_connection()

    try:
        rows = conn.execute(
            """
            SELECT id, distance, fare, search_date
            FROM search_history
            ORDER BY id DESC
            """
        ).fetchall()

        history = [dict(row) for row in rows]

        return jsonify({
            "status": "success",
            "history": history
        }), 200

    except sqlite3.Error:
        return jsonify({
            "status": "error",
            "message": "Could not retrieve search history"
        }), 500

    finally:
        conn.close()

# Merged the duplicate runner blocks into one to fix the error
if __name__ == '__main__':
    init_db()
    # host='0.0.0.0' lagane se cloud server external browser ke liye open ho jata hai
    app.run(host='0.0.0.0', port=5000, debug=True)
