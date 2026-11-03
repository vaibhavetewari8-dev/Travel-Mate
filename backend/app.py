from flask import Flask, render_template, request, jsonify
import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, '..', 'frontend'))
DB_PATH = os.path.join(BASE_DIR, '..', 'database', 'travelmate.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS search_history (id INTEGER PRIMARY KEY AUTOINCREMENT, distance REAL, fare REAL)")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/save_search', methods=['POST'])
def save_search():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO search_history (distance, fare) VALUES (?, ?)", (data.get('distance'), data.get('fare')))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
