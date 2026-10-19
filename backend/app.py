# app.py (Yuvraj)
from flask import Flask, render_template

app = Flask(__name__)

# Main route jo Shreya ka frontend render karega
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Debug mode ON taaki development ke time changes instantly dikhein
    app.run(debug=True, port=5000)

