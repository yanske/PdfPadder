import os
import sys

from flask import Flask, flash, redirect, render_template, request, send_file
from werkzeug.utils import secure_filename

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))
from padder import padder

app = Flask(__name__)
app.secret_key = "SECRET"
app.config['UPLOAD_FOLDER'] = '/tmp'

@app.route('/')
def index():
    return render_template('index.html')

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

    output = padder.pad_pdf(path, 0.4)
    # TODO: remove the PDF once it has been processed.
    return send_file(output, as_attachment=True)

if __name__ == '__main__':
    app.run()
