# app.py (Yuvraj)
from flask import Flask, render_template
from flask import request, jsonify
import sqlite3

app = Flask(__name__)

# Main route jo Shreya ka frontend render karega
@app.route('/')
def home():
    return render_template('index.html')

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('travelmate.db')
    conn.row_factory = sqlite3.Row
    return conn


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

if __name__ == '__main__':
    # Debug mode ON taaki development ke time changes instantly dikhein
    app.run(debug=True, port=5000)
