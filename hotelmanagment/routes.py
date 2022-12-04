from flask import render_template, url_for, flash, redirect, request
from hotelmanagment import app, db, bcrypt
from hotelmanagment.forms import HotelForm, RegistrationForm, LoginForm
from hotelmanagment.models import User
from flask_login import login_user, current_user, logout_user, login_required

#For seeing if the login user is the admin user.
adminEmail = 'hotelmanagment213@gmail.com'
adminPassword = 'AdminView'

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
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login', 'success')
        return redirect(url_for('login')) 
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        flash(f'You have been logged in!', 'success') #NOT WORKING! The message fails to pop up.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('hotel_form')) # This needs to be re-routed to the home page which will have an account button which would then hold reservation page information via hotel_form.
        elif form.email.data == adminEmail and form.password.data == adminPassword: #Checks if the login user is the admin user.
            flash(f"Greetings Hotel Palm Aire Manager!\n Here is your list of clients currently reserved for rooms.")
            return redirect(url_for('admin_view'))
        flash(f'Login Unsuccessful. Please check username and password', 'danger') #NOT WORKING! The message fails to pop up.
    return render_template('login.html', title='Login', form=form) 

#Page where the user inputs their information about the stay.
@app.route("/hotel_form", methods=['GET', 'POST'])
def hotel_form():
    form = HotelForm()
    if form.validate_on_submit():
        flash(f'Room registered for {form.name.data}. We hope you enjoy your stay!', 'success')
        return redirect(url_for('client_view'))
    return render_template('hotel_form.html', title='Hotel Form', form=form) 

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/admin_view")
def admin_view():
    return render_template('admin_view.html', title='Admin View', clients=clients)

@app.route("/client_view")
def client_view():
    return render_template('client_view.html', title='Client View', clients=clients)

    
