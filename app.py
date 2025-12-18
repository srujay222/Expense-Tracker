# app.py
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Function to connect to Database
def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the table if it doesn't exist
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, item TEXT, amount REAL, category TEXT)')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    
    # If user submitted the form (POST)
    if request.method == 'POST':
        item = request.form['item']
        amount = request.form['amount']
        category = request.form['category']
        # SQL Query to insert data
        conn.execute("INSERT INTO expenses (item, amount, category) VALUES (?, ?, ?)", (item, amount, category))
        conn.commit()
    
    # Get all expenses to show in the table
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

if __name__ == '__main__':
    init_db() # Run DB setup once
    app.run(debug=True)
