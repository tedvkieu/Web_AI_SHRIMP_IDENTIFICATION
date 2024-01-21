from flask import Flask, redirect, url_for,render_template, send_from_directory,request, send_file,jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os 
from wtforms.validators import InputRequired
import requests
from io import BytesIO
from PIL import Image
from urllib.parse import urlparse


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/images/img_process'


class uploadFileForm(FlaskForm):
    file = FileField("File", validators = [InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename) 

@app.route('/', methods = ['GET', 'POST'])
def index():
   form = uploadFileForm()
   if form.validate_on_submit():
       file = form.file.data
       
       filename = secure_filename(file.filename)
       file_url = url_for('get_file', filename = filename)
       file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
   else:
        file_url = None    
   return render_template("index.html", form = form, file_url = file_url)

@app.route('/user/<name>')
def hello_user(name):
    return f"<h1> Hello {name}</h1>"

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    return f"<h1> Blog thu {blog_id}</h1>"

@app.route('/authors/<username>')
def show_author(username):
   return render_template('profile.html', username=username)

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data['url']
        
        response = requests.get(url)
        img_data = BytesIO(response.content)
        
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        filename = get_filename_from_url(url)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(image_path, 'wb') as f:
            f.write(img_data.getvalue())
        
        return jsonify({'success': True, 'image_path': image_path})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    app.run(debug = True)