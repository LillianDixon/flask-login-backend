from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# the most important part of the flask-login is the LoginManager
login_manager = LoginManager()
# login manager contains the code that lets your app and flask-login work together
    # how to load a user from an ID
    # Where to send users when they need to login

app.config["SQLALCHEMY_DATABASE_URI"]=''
heroku = Heroku(app)
db = SQLAlchemy(app)


# configure the app for login
login_manager.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    author = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True
        # returns true if the user is authenticated

    def is_active(self):
        return True
        # returns true if the user is active

    def get_id(self):
        return self.email
        # return the email address to stisfy flask-login's requrements
        # provides a unicode ID

    def __repr__(self):
        return '<User %r>' % (self.username)


# you have to provide a user_loader callback.  This callback is used to reload the user object from the user ID stored in the session.
# It should take the unicode ID and return the corresponding user object
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def home():
    return"<h1>Hi from Flask</h1>"


if __name__ == "__main__":
    app.debug = True
    app.run()