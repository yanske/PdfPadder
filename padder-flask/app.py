import os
import sys

from flask import Flask, flash, redirect, render_template, request, send_file
from werkzeug.utils import secure_filename

# Includes the parent directory, to allow importing the padder module.
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
    if not pdf.filename.endswith('.pdf'):
        flash("Not a PDF file!")
        return redirect('/')

    # Save the file into a temp location.
    filename = secure_filename(pdf.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf.save(path)

    try:
        output = padder.pad_pdf(path, 0.4)
        return send_file(output, as_attachment=True)
    except Exception as e:
        flash("Error: " + str(e))
        return redirect('/')

if __name__ == '__main__':
    app.run()
