from flask import Flask, render_template, request 
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Booking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            design TEXT,
            length TEXT,
            glitter TEXT,
            total TEXT
        )
    ''')

    # Contact table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()

def init_db():
    init_db()
 


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/customized')
def customized():
    return render_template('customized.html')

@app.route('/discover')
def discover():
    return render_template('discover.html')

@app.route('/book')
def booking():
    return render_template('book.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')



# Booking from customized page
# @app.route('/book', methods=['POST'])
# def book():
#     design = request.form.get('design')
#     length = request.form.get('length')
#     glitter = request.form.get('glitter')
#     total = request.form.get('total')

#     return render_template('book.html',
#                            design=design,
#                            length=length,
#                            glitter=glitter,
#                            total=total)


@app.route('/book', methods=['POST'])
def book():
    design = request.form.get('design')
    length = request.form.get('length')
    glitter = request.form.get('glitter')
    total = request.form.get('total')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO bookings (design, length, glitter, total)
        VALUES (?, ?, ?, ?)
    ''', (design, length, glitter, total))

    conn.commit()
    conn.close()

    return render_template('book.html',
                           design=design,
                           length=length,
                           glitter=glitter,
                           total=total)

@app.route('/confirm', methods=['POST'])
def confirm():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    date = request.form.get('date')
    time = request.form.get('time')
    design = request.form.get('design')
    event = request.form.getlist('event')  # for checkboxes

    return f"Thank you {name}, your booking is confirmed!"

@app.route('/contact_submit', methods=['POST'])
def contact_submit():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO contacts (name, email, message)
        VALUES (?, ?, ?)
    ''', (name, email, message))

    conn.commit()
    conn.close()

    return "Message Sent Successfully!"


# @app.route('/contact_submit', methods=['POST'])
# def contact_submit():
#     name = request.form.get('name')
#     email = request.form.get('email')
#     subject = request.form.get('subject')
#     message = request.form.get('message')

#     print("New Contact Message:")
#     print(name, email, subject, message)

#     return f"Thank you {name}, your message has been sent!"
@app.route('/view_bookings')
def view_bookings():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    data = cursor.fetchall()

    conn.close()
    return str(data)

@app.route('/view_contacts')
def view_contacts():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()

    conn.close()
    return str(data)

if __name__ == "__main__":
    app.run(debug=True)