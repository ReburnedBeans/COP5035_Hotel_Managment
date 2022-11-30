from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy #For using SQLAlchemy
from forms import HotelForm, RegistrationForm, LoginForm

#For seeing if the login user is the admin user.
adminEmail = 'hotelmanagment213@gmail.com'
adminPassword = 'AdminView'

app = Flask(__name__)
app.config['SECRET_KEY'] = '1c0f66335b647802e2f8e872def6e6dbd5544841bd963025f2c77a32966fd2cb' #Random Secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #For using SQLAlchemy
db = SQLAlchemy(app) #For using SQLAlchemy

#For using SQLAlchemy.
class User(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    number_of_nights = db.Column(db.Integer)
    room_type = db.Column(db.Integer)

db.create_all()

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


clients = [ #Debuggingg for the admin_view page. Plan on removing after DB is set up.
    {
        'username': 'Username1',
        'room_type': 'RoomType1',
        'number_of_nights': 'Number1'
    },
    {
        'username': 'Username2',
        'room_type': 'RoomType2',
        'number_of_nights': 'Number2'
    },
    {
        'username': 'Username3',
        'room_type': 'RoomType3',
        'number_of_nights': 'Number3'
    },
    {
        'username': 'Username4',
        'room_type': 'RoomType4',
        'number_of_nights': 'Number4'
    },
    {
        'username': 'Username5',
        'room_type': 'RoomType5',
        'number_of_nights': 'Number5'
    }
    ]



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('hotel_form'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('You have been logged in!', 'success') #NOT WORKING! The message fails to pop up.
        if form.email.data == adminEmail and form.password.data == adminPassword: #Checks if the login user is the admin user.
            return redirect(url_for('admin_view'))
        else:
            return redirect(url_for('hotel_form'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger') #NOT WORKING! The message fails to pop up.
    return render_template('login.html', title='Login', form=form) 

#Page where the user inputs their information about the stay.
@app.route("/hotel_form", methods=['GET', 'POST'])
def hotel_form():
    form = HotelForm()
    if form.validate_on_submit():
        flash(f'Room registered for {form.name.data}. We hope you enjoy your stay!', 'success')
        return redirect(url_for('home'))
    return render_template('hotel_form.html', title='Hotel Form', form=form) 

@app.route("/admin_view")
def admin_view():
    return render_template('admin_view.html', title='Admin View', clients=clients)


if __name__ == '__main__':
    app.run(debug=True)