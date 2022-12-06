from flask import Flask
from flask_sqlalchemy import SQLAlchemy #For using SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '1c0f66335b647802e2f8e872def6e6dbd5544841bd963025f2c77a32966fd2cb' #Random Secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #For using SQLAlchemy
db = SQLAlchemy(app) #For using SQLAlchemy
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from hotelmanagment import routes
from hotelmanagment.models import User

#For seeing if the login user is the admin user.
adminEmail = 'hotelmanagment213@gmail.com'
adminPassword = 'AdminView'
adminHashedPw = bcrypt.generate_password_hash(adminPassword).decode("utf-8")
adminUsername = "Manager"
managerFlag = False

with app.app_context():
    db.create_all()
    user = User.query.filter_by(email = adminEmail).first()
    if not user:
        user = User(username = adminUsername, email = adminEmail, password = adminHashedPw)
        db.session.add(user)
        db.session.commit()
    



