from flask import Flask, render_template, request, send_file, redirect, url_for
import qrcode
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    title = request.form['title']
    email = request.form['email']
    phone = request.form['phone']
    linkedin = request.form['linkedin']

    # Generate QR code
    qr_data = f"Name: {name}\nTitle: {title}\nEmail: {email}\nPhone: {phone}\nLinkedIn: {linkedin}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')

    # Save QR code image to a BytesIO object
    img_io = BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    # Save the image to a static folder
    img_path = 'static/business_card.png'
    qr_img.save(img_path)

    return render_template('result.html', img_path=img_path)

@app.route('/download')
def download():
    return send_file('static/business_card.png', mimetype='image/png', as_attachment=True, download_name='business_card.png')

if __name__ == '__main__':
    app.run(debug=True)
