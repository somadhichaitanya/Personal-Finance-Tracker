from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'data/finance.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions ORDER BY date DESC').fetchall()
    summary = conn.execute("SELECT type, SUM(amount) as total FROM transactions GROUP BY type").fetchall()
    conn.close()
    return render_template('index.html', transactions=transactions, summary=summary)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        t_type = request.form['type']
        date = request.form['date'] or datetime.today().strftime('%Y-%m-%d')

        conn = get_db_connection()
        conn.execute("INSERT INTO transactions (amount, category, type, date) VALUES (?, ?, ?, ?)",
                    (amount, category, t_type, date))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
