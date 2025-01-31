from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contact_form (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            email TEXT,
                            message TEXT)''')
        conn.commit()

# Home route to display form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Insert data into SQLite database
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contact_form (name, email, message) VALUES (?, ?, ?)", 
                           (name, email, message))
            conn.commit()

        return redirect('/thank_you')
    return render_template('index.html')

# Thank you page after form submission
@app.route('/thank_you')
def thank_you():
    return "Thank you for contacting us!"

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
