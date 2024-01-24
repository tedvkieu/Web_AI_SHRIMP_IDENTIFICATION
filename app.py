from flask import Flask, redirect, url_for,render_template, send_from_directory,request, send_file,jsonify, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from enum import EnumMeta
from os import path
import os 
from datetime import timedelta
from flask.helpers import flash
from wtforms.validators import InputRequired
import requests
from io import BytesIO
from PIL import Image
from urllib.parse import urlparse


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'static/images/img_process'
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/login', methods =["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form["name"]
        session.permanent=True
        if user_name:
            session["user"] = user_name
            found_user = User.query.filter_by(name = user_name).first()
            if found_user:
                session["email"] = found_user.email
            else:   
                user = User(user_name, 'temp@gmail.com')
                db.session.add(user)
                db.session.commit()
            flash("created in DB!")
            flash("you logged in successfully!", "info")
            return redirect(url_for("user", user = user_name))
        if "user" in session:
            name = session["user"]
            flash("you have already logged in!", "info")
            return redirect(url_for("user", user = user_name))
    return render_template("login.html")

@app.route('/user', methods = ["POST", "GET"])
def user():
    email = None

    if "user" in session:
       name = session["user"]
       if request.method == "POST":
           if not request.form["email"] and request.form["name"]:
               User.query.filter_by(name = name).delete()
               db.session.commit()
               flash("deleted user!")
               return redirect(url_for("log_out"))
           else:
                email = request.form["email"]
                session["email"] = email
                found_user = User.query.filter_by(name = name).first()
                found_user.email = email
                db.session.commit()
                flash("email updated")
       elif "email" in session:
           email = session["email"]
       return render_template("user.html", user = name, email = email)
    else:
        flash("you haven't logged in", "info")
        return redirect(url_for("login"))

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
    with app.app_context():
        if not path.exists("user.db"):
            db.create_all()
            print("Created database!")
        app.run(debug=True)