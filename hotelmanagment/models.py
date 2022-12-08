from hotelmanagment import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#For using SQLAlchemy.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship('Booking', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


#For using SQLAlchemy.
class Booking(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String(20), nullable=False)
    number_of_nights = db.Column(db.Integer)
    room_type = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Booking('{self.party_name}', '{self.number_of_nights}')"
