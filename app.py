from flask import Flask, render_template, request 

app = Flask(__name__)


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
def book():
    return render_template('book.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == "__main__":
    app.run(debug=True)

# Booking from customized page
@app.route('/book', methods=['POST'])
def book():
    design = request.form.get('design')
    length = request.form.get('length')
    glitter = request.form.get('glitter')
    total = request.form.get('total')

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

# Final booking submit
# @app.route('/confirm', methods=['POST'])
# def confirm():
#     name = request.form.get('name')
#     phone = request.form.get('phone')
#     date = request.form.get('date')

    # return render_template('success.html', name=name)


# Contact page
# @app.route('/contact')
# def contact():
#     return render_template('contact.html')


# # Contact form submit
# @app.route('/contact_submit', methods=['POST'])
# def contact_submit():
#     name = request.form.get('name')
#     message = request.form.get('message')

#     return f"Thank you {name}, we received your message!"

@app.route('/contact_submit', methods=['POST'])
def contact_submit():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    print("New Contact Message:")
    print(name, email, subject, message)

    return f"Thank you {name}, your message has been sent!"

