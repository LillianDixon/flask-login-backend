from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)

# the most important part of the flask-login is the LoginManager
login_manager = LoginManager()
# login manager contains the code that lets your app and flask-login work together
    # how to load a user from an ID
    # Where to send users when they need to login

app.secret_key = 'secretKey'
app.config["SQLALCHEMY_DATABASE_URI"]='postgres://fpsgyyfdqylmmf:339a68330c55fe4fbe0493882994f6865ae2b7d9b123cfb20fc04b83dc59b979@ec2-34-195-169-25.compute-1.amazonaws.com:5432/d7dcdknsgn7rfb'
heroku = Heroku(app)
db = SQLAlchemy(app)


# configure the app for login
login_manager.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')
        email = post_data.get('email')
        registered_user = User.query.filter_by(username=username, password=password, email = email).first()
        if registered_user is None:
            return jsonify('Username or password is invalid')
        login_user(registered_user)
        return jsonify('Logged in')
    return jsonify('something went wrong')

@app.route('/new-user', methods=['POST'])
def new_user():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')
        email = post_data.get('email')
        reg = User(username, password, email)
        db.session.add(reg)
        db.session.commit()
        return jsonify('User Created')
    return jsonify('Something went wrong')

@app.route('/get-users', methods=['GET'])
def get_users():
    all_users = db.session.query(User.id, User.username, User.password, User.email).all()
    return jsonify(all_users)


if __name__ == "__main__":
    app.debug = True
    app.run()