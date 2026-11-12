import os
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, session, redirect, url_for

# Base directory and SQLite database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'database.db')

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "palmglow_production_secret_key_2026")

ADMIN_PIN = os.environ.get("ADMIN_PIN", "palmglow2026")
COMPANY_EMAIL = os.environ.get("ALERT_EMAIL", "aashiga10806@gmail.com")


# ------------------ EMAIL NOTIFICATION SERVICE ------------------
def send_email_alert(subject, body_html):
    """
    Sends an instant email notification to the business owner.
    Configurable via Replit Secrets (MAIL_USERNAME and MAIL_PASSWORD).
    Fails safely without breaking user requests if credentials aren't set.
    """
    sender = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")
    recipient = COMPANY_EMAIL

    if not sender or not password:
        # Email credentials not yet configured in Replit Secrets
        print("💡 [EMAIL NOTICE] Set MAIL_USERNAME and MAIL_PASSWORD in Replit Secrets for automatic Gmail alerts.")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = f"Palm Glow Notifications <{sender}>"
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body_html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"📧 [EMAIL DELIVERED] Alert sent to {recipient}")
        return True
    except Exception as e:
        print(f"⚠️ [EMAIL FAILED] {e}")
        return False


# ------------------ DATABASE INITIALIZATION ------------------
def init_db():
    """Initializes and migrates database tables so no data or columns are lost."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Bookings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            date TEXT,
            time TEXT,
            event TEXT,
            design TEXT,
            length TEXT,
            glitter TEXT,
            total TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Safely migrate existing bookings table if created with old schema
    cursor.execute("PRAGMA table_info(bookings)")
    existing_booking_cols = [col[1] for col in cursor.fetchall()]
    all_booking_cols = ['name', 'phone', 'email', 'address', 'date', 'time', 'event', 'design', 'length', 'glitter', 'total', 'created_at']
    for col in all_booking_cols:
        if col not in existing_booking_cols:
            cursor.execute(f"ALTER TABLE bookings ADD COLUMN {col} TEXT")

    # 2. Contacts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            subject TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Safely migrate existing contacts table
    cursor.execute("PRAGMA table_info(contacts)")
    existing_contact_cols = [col[1] for col in cursor.fetchall()]
    all_contact_cols = ['subject', 'created_at']
    for col in all_contact_cols:
        if col not in existing_contact_cols:
            cursor.execute(f"ALTER TABLE contacts ADD COLUMN {col} TEXT")

    conn.commit()
    conn.close()


# Ensure tables are ready at startup (both local and under Gunicorn on Replit)
init_db()


# ------------------ PUBLIC CLIENT ROUTES ------------------

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


# ------------------ CUSTOMIZED DESIGN FLOW ------------------

@app.route('/customized', methods=['GET', 'POST'])
def customized():
    if request.method == 'POST':
        design_val = request.form.get('design')
        length = request.form.get('length')
        glitter = request.form.get('glitter') or "No"
        total = request.form.get('total')

        print("\n" + "-" * 50)
        print("🎨 [CUSTOM DESIGN SELECTED]")
        print(f"   Design : {design_val}")
        print(f"   Length : {length}")
        print(f"   Glitter: {glitter}")
        print(f"   Total  : ₹{total}")
        print("-" * 50 + "\n")

        return render_template('book.html',
                               design=design_val,
                               length=length,
                               glitter=glitter,
                               total=total)

    return render_template('customized.html')


# ------------------ CONFIRM BOOKING (SAVES TO DB & ALERTS) ------------------

@app.route('/confirm', methods=['POST'])
def confirm():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    address = request.form.get('address', '').strip()
    date = request.form.get('date', '').strip()
    time = request.form.get('time', '').strip()
    design_val = request.form.get('design', '').strip()
    length = request.form.get('length', '').strip()
    glitter = request.form.get('glitter', '').strip()
    total = request.form.get('total', '').strip()

    events = request.form.getlist('event')
    other_event = request.form.get('other_event', '').strip()
    if other_event:
        events.append(f"Other: {other_event}")
    event_str = ", ".join(events) if events else "General"

    # 1. Save to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (name, phone, email, address, date, time, event, design, length, glitter, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, email, address, date, time, event_str, design_val, length, glitter, total))
    conn.commit()
    conn.close()

    # 2. Terminal Activity Logging
    print("\n" + "=" * 55)
    print("✨ [NEW BOOKING STORED IN DATABASE]")
    print(f"   Customer : {name}")
    print(f"   Phone    : {phone}")
    print(f"   Email    : {email}")
    print(f"   Date/Time: {date} at {time}")
    print(f"   Event    : {event_str}")
    print(f"   Design   : {design_val}")
    if total:
        print(f"   Total    : ₹{total}")
    print(f"   Address  : {address}")
    print("   Status   : Saved to database.db successfully!")
    print("=" * 55 + "\n")

    # 3. Trigger Email Alert to Owner
    email_html = f"""
    <h2>✨ New Booking Received - Palm Glow</h2>
    <p><strong>Customer:</strong> {name}</p>
    <p><strong>Phone:</strong> {phone}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Date & Time:</strong> {date} at {time}</p>
    <p><strong>Design:</strong> {design_val}</p>
    <p><strong>Event:</strong> {event_str}</p>
    <p><strong>Estimated Total:</strong> ₹{total if total else 'Standard'}</p>
    <p><strong>Address:</strong> {address}</p>
    """
    send_email_alert(f"✨ New Booking from {name} ({date})", email_html)

    return render_template('success.html',
                           title="Booking Confirmed",
                           headline=f"Thank You, {name}!",
                           message="Your appointment request has been successfully registered. Our team will contact you shortly to confirm the appointment.",
                           details={
                               'Customer Name': name,
                               'Phone': phone,
                               'Appointment Date': f"{date} at {time}",
                               'Design': design_val,
                               'Event Type': event_str,
                               'Estimated Total': f"₹{total}" if total else "Standard Pricing"
                           })


# ------------------ CONTACT FORM SUBMISSION ------------------

@app.route('/contact_submit', methods=['POST'])
def contact_submit():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    # 1. Save to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts (name, email, subject, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, subject, message))
    conn.commit()
    conn.close()

    # 2. Terminal Activity Logging
    print("\n" + "=" * 55)
    print("📩 [NEW CONTACT MESSAGE STORED IN DATABASE]")
    print(f"   From   : {name} ({email})")
    print(f"   Subject: {subject}")
    print(f"   Message: {message}")
    print("   Status : Saved to database.db successfully!")
    print("=" * 55 + "\n")

    # 3. Trigger Email Alert to Owner
    email_html = f"""
    <h2>📩 New Contact Message - Palm Glow</h2>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Subject:</strong> {subject}</p>
    <p><strong>Message:</strong></p>
    <blockquote>{message}</blockquote>
    <hr>
    <p><a href="mailto:{email}?subject=Re: {subject}">Reply to Customer</a></p>
    """
    send_email_alert(f"📩 Contact Message from {name}: {subject}", email_html)

    return render_template('success.html',
                           title="Message Sent",
                           headline=f"Thank You, {name}!",
                           message="Your message has been sent and stored. We will reply to your inquiry as soon as possible.",
                           details={
                               'Name': name,
                               'Email': email,
                               'Subject': subject,
                               'Message': message
                           })


# ------------------ SECURE COMPANY ADMIN DASHBOARD ------------------

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Handle Login Form
    if request.method == 'POST':
        pin = request.form.get('pin', '').strip()
        if pin == ADMIN_PIN:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_admin_login(error="Incorrect PIN. Please try again.")

    # Check Login Status or query param override
    pin_arg = request.args.get('pin', '')
    if pin_arg == ADMIN_PIN:
        session['admin_logged_in'] = True

    if not session.get('admin_logged_in'):
        return render_admin_login()

    # Load Data from Database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
    bookings = cursor.fetchall()
    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    contacts = cursor.fetchall()
    conn.close()

    return render_admin_dashboard(bookings, contacts)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin'))


# Backwards compatibility routes redirect to admin
@app.route('/view_bookings')
def view_bookings():
    return redirect(url_for('admin'))

@app.route('/view_contacts')
def view_contacts():
    return redirect(url_for('admin'))


# ------------------ ADMIN HTML TEMPLATES (BUILT-IN) ------------------

def render_admin_login(error=None):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Login - Palm Glow</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    </head>
    <body class="bg-light d-flex align-items-center min-vh-100">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-5 col-lg-4">
                    <div class="card shadow-lg border-0 rounded-4 p-4 text-center">
                        <div class="mb-3">
                            <i class="fa-solid fa-lock text-warning" style="font-size: 3rem;"></i>
                        </div>
                        <h3 class="fw-bold mb-1" style="color: maroon;">Palm Glow Portal</h3>
                        <p class="text-muted small mb-4">Company Administration</p>

                        {"<div class='alert alert-danger py-2 small'>" + error + "</div>" if error else ""}

                        <form method="POST" action="/admin">
                            <div class="mb-3">
                                <input type="password" name="pin" class="form-control text-center py-2 fs-5" placeholder="Enter Admin PIN" required autofocus>
                                <small class="text-muted d-block mt-1">Default PIN: <code>palmglow2026</code></small>
                            </div>
                            <button type="submit" class="btn text-white w-100 py-2 fw-semibold" style="background-color: maroon;">
                                Unlock Dashboard
                            </button>
                        </form>
                        <div class="mt-4">
                            <a href="/" class="text-decoration-none text-muted small">← Back to Website</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


def render_admin_dashboard(bookings, contacts):
    bookings_rows = ""
    for r in bookings:
        clean_phone = (r['phone'] or '').replace('+', '').replace(' ', '').replace('-', '')
        wa_link = f"https://wa.me/{clean_phone}?text=Hello%20{r['name']},%20this%20is%20Palm%20Glow%20Mehandi%20Arts%20regarding%20your%20booking%20for%20{r['date']}." if clean_phone else "#"
        call_link = f"tel:{clean_phone}" if clean_phone else "#"
        mail_link = f"mailto:{r['email']}" if r['email'] else "#"

        bookings_rows += f"""
        <tr>
            <td><strong>#{r['id']}</strong></td>
            <td>
                <div class="fw-bold">{r['name'] or 'Anonymous'}</div>
                <small class="text-muted"><i class="fa-solid fa-location-dot me-1"></i>{r['address'] or 'N/A'}</small>
            </td>
            <td>
                <div><a href="{call_link}" class="text-decoration-none"><i class="fa-solid fa-phone me-1"></i>{r['phone'] or 'N/A'}</a></div>
                <small><a href="{mail_link}" class="text-muted text-decoration-none">{r['email'] or ''}</a></small>
            </td>
            <td>
                <div class="fw-semibold">{r['date'] or 'TBD'}</div>
                <small class="text-muted">{r['time'] or ''}</small>
            </td>
            <td><span class="badge bg-warning text-dark">{r['design'] or 'Standard'}</span></td>
            <td><span class="badge bg-secondary">{r['event'] or 'General'}</span></td>
            <td class="fw-bold text-success">₹{r['total'] or '0'}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <a href="{wa_link}" target="_blank" class="btn btn-outline-success" title="WhatsApp Customer">
                        <i class="fa-brands fa-whatsapp"></i> Chat
                    </a>
                    <a href="{call_link}" class="btn btn-outline-primary" title="Call Customer">
                        <i class="fa-solid fa-phone"></i>
                    </a>
                </div>
            </td>
        </tr>
        """

    contacts_rows = ""
    for c in contacts:
        reply_link = f"mailto:{c['email']}?subject=Re: {c['subject'] or 'Inquiry'}" if c['email'] else "#"
        contacts_rows += f"""
        <tr>
            <td><strong>#{c['id']}</strong></td>
            <td class="fw-bold">{c['name'] or 'N/A'}</td>
            <td><a href="{reply_link}">{c['email'] or 'N/A'}</a></td>
            <td><span class="badge bg-info text-dark">{c['subject'] or 'General Inquiry'}</span></td>
            <td>{c['message'] or ''}</td>
            <td class="small text-muted">{c['created_at'] or ''}</td>
            <td>
                <a href="{reply_link}" class="btn btn-sm btn-outline-primary">
                    <i class="fa-solid fa-reply"></i> Reply
                </a>
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Company Dashboard - Palm Glow</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    </head>
    <body class="bg-light">
        <nav class="navbar navbar-dark bg-dark px-4 py-3 shadow">
            <div class="container-fluid">
                <span class="navbar-brand mb-0 h1 fw-bold">
                    <i class="fa-brands fa-sketch text-warning me-2"></i> Palm Glow - Business Management
                </span>
                <div>
                    <a href="/" target="_blank" class="btn btn-sm btn-outline-light me-2">
                        <i class="fa-solid fa-globe me-1"></i> View Live Website
                    </a>
                    <a href="/admin/logout" class="btn btn-sm btn-danger">
                        <i class="fa-solid fa-right-from-bracket me-1"></i> Logout
                    </a>
                </div>
            </div>
        </nav>

        <div class="container my-5">
            <!-- Metrics Cards -->
            <div class="row g-4 mb-4">
                <div class="col-md-6 col-lg-4">
                    <div class="card shadow-sm border-0 border-start border-warning border-4 p-3 bg-white">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <div class="text-muted small fw-semibold">TOTAL APPOINTMENTS</div>
                                <div class="fs-2 fw-bold text-dark">{len(bookings)}</div>
                            </div>
                            <i class="fa-solid fa-calendar-check text-warning fs-1"></i>
                        </div>
                    </div>
                </div>

                <div class="col-md-6 col-lg-4">
                    <div class="card shadow-sm border-0 border-start border-primary border-4 p-3 bg-white">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <div class="text-muted small fw-semibold">CONTACT INQUIRIES</div>
                                <div class="fs-2 fw-bold text-dark">{len(contacts)}</div>
                            </div>
                            <i class="fa-solid fa-envelope-open-text text-primary fs-1"></i>
                        </div>
                    </div>
                </div>

                <div class="col-md-6 col-lg-4">
                    <div class="card shadow-sm border-0 border-start border-success border-4 p-3 bg-white">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <div class="text-muted small fw-semibold">SYSTEM STATUS</div>
                                <div class="fs-4 fw-bold text-success">Active 24/7</div>
                            </div>
                            <i class="fa-solid fa-circle-check text-success fs-1"></i>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tabbed View -->
            <div class="card shadow-sm border-0 rounded-4 p-4 bg-white">
                <ul class="nav nav-pills mb-4" id="adminTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active fw-semibold" id="bookings-tab" data-bs-toggle="pill" data-bs-target="#bookings-pane" type="button">
                            <i class="fa-solid fa-calendar-days me-2"></i> Bookings ({len(bookings)})
                        </button>
                    </li>
                    <li class="nav-item ms-2" role="presentation">
                        <button class="nav-link fw-semibold" id="contacts-tab" data-bs-toggle="pill" data-bs-target="#contacts-pane" type="button">
                            <i class="fa-solid fa-message me-2"></i> Contact Messages ({len(contacts)})
                        </button>
                    </li>
                </ul>

                <div class="tab-content" id="adminTabsContent">
                    <!-- Bookings Pane -->
                    <div class="tab-pane fade show active" id="bookings-pane" role="tabpanel">
                        <div class="table-responsive">
                            <table class="table table-hover align-middle">
                                <thead class="table-light">
                                    <tr>
                                        <th>ID</th>
                                        <th>Client</th>
                                        <th>Contact Info</th>
                                        <th>Date & Time</th>
                                        <th>Design</th>
                                        <th>Event</th>
                                        <th>Price</th>
                                        <th>Quick Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {bookings_rows if bookings_rows else "<tr><td colspan='8' class='text-center py-4 text-muted'>No bookings recorded yet.</td></tr>"}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Contacts Pane -->
                    <div class="tab-pane fade" id="contacts-pane" role="tabpanel">
                        <div class="table-responsive">
                            <table class="table table-hover align-middle">
                                <thead class="table-light">
                                    <tr>
                                        <th>ID</th>
                                        <th>Sender Name</th>
                                        <th>Email</th>
                                        <th>Subject</th>
                                        <th>Message</th>
                                        <th>Sent At</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {contacts_rows if contacts_rows else "<tr><td colspan='7' class='text-center py-4 text-muted'>No contact messages recorded yet.</td></tr>"}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """


# ------------------ SERVER RUNNER (REPLIT & LOCAL) ------------------
if __name__ == "__main__":
    # In Replit, web services bind to port 8080 or the PORT env var; locally defaults to 5000
    is_replit = bool(os.environ.get("REPL_ID") or os.environ.get("REPLIT_ENVIRONMENT"))
    default_port = 8080 if is_replit else 5000
    port = int(os.environ.get("PORT", default_port))
    debug = os.environ.get("FLASK_DEBUG", "False" if is_replit else "True").lower() == "true"

    print("\n" + "=" * 60)
    print("🌟 Palm Glow Company Web Application Active!")
    print(f"   Environment : {'Replit Cloud Deployment' if is_replit else 'Local Development'}")
    print(f"   Listening on: http://0.0.0.0:{port}")
    print(f"   Database    : {db_path}")
    print(f"   Admin Portal: /admin (Default PIN: {ADMIN_PIN})")
    print("=" * 60 + "\n")

    app.run(host="0.0.0.0", port=port, debug=debug)
