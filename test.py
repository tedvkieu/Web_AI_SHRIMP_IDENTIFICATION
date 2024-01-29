from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
import os
from werkzeug.utils import secure_filename
import urllib.request

# the "files" directory next to the app.py file
#UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
#print(UPLOAD_FOLDER)
UPLOAD_FOLDER = 'static/images/img_process'
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'Sick Rat'
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
@app.route('/')
def index(): 
    return render_template('upload.html')
  
@app.route('/', methods=['POST'])
def upload():
    if 'uploadFile[]' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('uploadFile[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            msg  = 'File successfully uploaded to /static/uploads!'
        else:
            msg  = 'Invalid Uplaod only png, jpg, jpeg, gif'
    return jsonify({'htmlresponse': render_template('response.html', msg=msg, filenames=file_names)})
 
def _get_files():
    file_list = os.path.join(UPLOAD_FOLDER, 'files.json')
    if os.path.exists(file_list):
        with open(file_list) as fh:
            return json.load(fh)
    return {}