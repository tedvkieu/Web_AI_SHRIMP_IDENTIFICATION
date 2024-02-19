import pyrebase

from flask import Flask, session, redirect, request, render_template

app = Flask(__name__)


config = {
    "apiKey": "AIzaSyDtkGxX2RktdG225UIkckVWYp8DOpJ4yyk",
    "authDomain": "fir-flask-login.firebaseapp.com",
    "projectId": "fir-flask-login",
    "storageBucket": "fir-flask-login.appspot.com",
    "messagingSenderId": "793015206279",
    "appId": "1:793015206279:web:debaf7f5bafe2c63ebd322",
    "measurementId": "G-23RZ9QEL7V",
    "databaseURL": ""
}

app.secret_key = "Kieune"
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/', methods=['POST', 'GET'])
def index():
    if('user' in session):
        return 'Hi, {}'.format(session['user'])
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
        except:
            return "failed to login"
    return render_template('test.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(port =1111)