import pyrebase


config = {
    'apiKey': "AIzaSyDtkGxX2RktdG225UIkckVWYp8DOpJ4yyk",
  'authDomain': "fir-flask-login.firebaseapp.com",
  'projectId': "fir-flask-login",
  'storageBucket': "fir-flask-login.appspot.com",
  'messagingSenderId': "793015206279",
  'appId': "1:793015206279:web:debaf7f5bafe2c63ebd322",
  'measurementId': "G-23RZ9QEL7V",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = 'test@gmail.com'
password = '123456'

#user = auth.create_user_with_email_and_password(email, password)
#print(user)

user = auth.sign_in_with_email_and_password(email, password)

#info = auth.get_account_info(user[`idToken`])
#print(info)

#auth.send_email_verification(user[`idToken`])

auth.send_password_reset_email(email)