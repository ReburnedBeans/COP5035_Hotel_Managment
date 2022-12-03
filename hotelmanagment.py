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

with app.app_context():
    db.create_all()

#For using SQLAlchemy.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    number_of_nights = db.Column(db.Integer)
    room_type = db.Column(db.Integer)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


clients = [ #Debugging for the admin_view page. Plan on removing after DB is set up.
    {
        'username': 'Samantha R',
        'room_type': '1-room small',
        'number_of_nights': '4'
    },
    {
        'username': 'Alexander S',
        'room_type': '1-room large',
        'number_of_nights': '2'
    },
    {
        'username': 'John H',
        'room_type': '2-room medium',
        'number_of_nights': '5'
    },
    {
        'username': 'Paul F',
        'room_type': '2-room large',
        'number_of_nights': '2'
    },
    {
        'username': 'John B',
        'room_type': '1-room large',
        'number_of_nights': '7'
    }
    ]



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


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
        return redirect(url_for('client_view'))
    return render_template('hotel_form.html', title='Hotel Form', form=form) 

@app.route("/admin_view")
def admin_view():
    return render_template('admin_view.html', title='Admin View', clients=clients)

@app.route("/client_view")
def client_view():
    return render_template('client_view.html', title='Client View', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)