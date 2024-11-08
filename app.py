from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup (initialize the database)
def init_db():
    conn = sqlite3.connect('hotel_bookings.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        check_in_date TEXT NOT NULL,
        check_out_date TEXT NOT NULL,
        room_type TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Home route - View all bookings
@app.route('/')
def home():
    conn = sqlite3.connect('hotel_bookings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()
    conn.close()
    return render_template('index.html', bookings=bookings)

# Create route - Add a new booking
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        room_type = request.form['room_type']

        # Insert new booking into database
        conn = sqlite3.connect('hotel_bookings.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO bookings (name, email, check_in_date, check_out_date, room_type)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, email, check_in_date, check_out_date, room_type))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))  # Redirect to homepage to see all bookings

    return render_template('create.html')

# Update route - Modify an existing booking
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = sqlite3.connect('hotel_bookings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE id = ?', (id,))
    booking = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        room_type = request.form['room_type']

        # Update booking in the database
        conn = sqlite3.connect('hotel_bookings.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE bookings
        SET name = ?, email = ?, check_in_date = ?, check_out_date = ?, room_type = ?
        WHERE id = ?
        ''', (name, email, check_in_date, check_out_date, room_type, id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))  # Redirect to homepage

    return render_template('update.html', booking=booking)

# Delete route - Delete a booking
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        # Delete booking from database
        conn = sqlite3.connect('hotel_bookings.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bookings WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))  # Redirect to homepage

    return render_template('delete.html', id=id)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)

