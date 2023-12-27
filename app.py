from flask import Flask, redirect, url_for,render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os 
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/images/img_process'

class uploadFileForm(FlaskForm):
    file = FileField("File", validators = [InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods = ['GET', 'POST'])
def index():
   form = uploadFileForm()
   if form.validate_on_submit():
       file = form.file.data
       file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
       return "File has been uploaded"
   return render_template("index.html", form = form )

@app.route('/user/<name>')
def hello_user(name):
    return f"<h1> Hello {name}</h1>"

@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    return f"<h1> Blog thu {blog_id}</h1>"

@app.route('/authors/<username>')
def show_author(username):
   return render_template('profile.html', username=username)

if __name__ == "__main__":
    app.run(debug = True)