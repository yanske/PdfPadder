import os
from flask import Flask, flash, redirect, render_template, request, send_file
from werkzeug.utils import secure_filename

import pdf2image
import img2pdf
from PIL import Image

import random
import string

app = Flask(__name__)
app.secret_key = "SECRET"
app.config['UPLOAD_FOLDER'] = '/tmp'

@app.route('/')
def index():
    return render_template('index.html')

def generate_tmp_path(ext = ''):
    letters = string.ascii_lowercase
    path = ''.join(random.choice(letters) for _ in range(10)) + ext
    return os.path.join(app.config['UPLOAD_FOLDER'], path)

def pad_pdf(path):
    # TODO: allow padding parameters to be passed.
    images = pdf2image.convert_from_path(path)

    # Pad the individual images.
    padded_images = []
    for img in images:
        w, h = img.size
        padded_img = Image.new("RGB", (int(w * 1.4), h), "white")
        padded_img.paste(img, (0, 0))

        padded_images.append(padded_img)

    # Save the images as files.
    image_paths = []
    for img in padded_images:
        tmp_path = generate_tmp_path('.jpeg')
        img.save(tmp_path, "JPEG")
        image_paths.append(tmp_path)

    # Output as PDF.
    output = generate_tmp_path('.pdf')
    with open(output, 'wb') as f:
        f.write(img2pdf.convert(image_paths))
    
    # Clean up temp image files used.
    for tmp_img in image_paths:
        os.remove(tmp_img)

    return output

@app.route('/pad', methods=['GET', 'POST'])
def pad():
    if 'pdf' not in request.files:
        flash("PDF not uploaded!")
        return redirect('/')
    
    pdf = request.files['pdf']
    # TODO: add validation on size and extension.

    # Save the file into a temp location.
    filename = secure_filename(pdf.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf.save(path)

    output = pad_pdf(path)
    # TODO: remove the PDF once it has been processed.
    return send_file(output, as_attachment=True)

if __name__ == '__main__':
    app.run()
