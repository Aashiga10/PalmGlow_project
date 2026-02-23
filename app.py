from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home → Customized Page
@app.route('/')
def home():
    return render_template('customized.html')


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


# Final booking submit
@app.route('/confirm', methods=['POST'])
def confirm():
    name = request.form.get('name')
    phone = request.form.get('phone')
    date = request.form.get('date')

    return render_template('success.html', name=name)


# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Contact form submit
@app.route('/contact_submit', methods=['POST'])
def contact_submit():
    name = request.form.get('name')
    message = request.form.get('message')

    return f"Thank you {name}, we received your message!"



if __name__ == '__main__':
    app.run(debug=True)