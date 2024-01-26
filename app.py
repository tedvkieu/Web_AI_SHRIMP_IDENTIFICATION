from flask import Flask, redirect, url_for,render_template, send_from_directory,request, send_file,jsonify, session, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from enum import EnumMeta
from werkzeug.utils import secure_filename
from datetime import timedelta
from flask.helpers import flash
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from io import BytesIO
from PIL import Image
from flask import *
from os import path

import os 
import json
import uuid
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'static/images/img_process'
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))


@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("project"))
        else:
            flash("Username or Password does not exist", 'error')
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        # Check if username or email already exists
        existing_user = user.query.filter((user.username == uname) | (user.email == mail)).first()
        if existing_user:
            flash("Username or Email already exists", 'error')
        else:
            # Create a new user if username and email are unique
            new_user = user(username=uname, email=mail, password=passw)
            db.session.add(new_user)
            try:
                db.session.commit()
                flash("Account created successfully", 'success')
                return redirect(url_for("login"))
                
            except IntegrityError:
                db.session.rollback()
                flash("An error occurred while creating the account", 'error')
    return render_template("register.html")

class uploadFileForm(FlaskForm):
    file = FileField("File", validators = [InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename) 

@app.route('/project', methods = ['GET', 'POST'])
def project():
   form = uploadFileForm()
   if form.validate_on_submit():
       file = form.file.data
       
       filename = secure_filename(file.filename)
       file_url = url_for('get_file', filename = filename)
       file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
   else:
        file_url = None    
   return render_template("project.html", form = form, file_url = file_url)

@app.route('/')
def index():
    return render_template("index.html")

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
    with app.app_context():
        if not path.exists("user.db"):
            db.create_all()
            print("Created database!")
        app.run(debug=True)