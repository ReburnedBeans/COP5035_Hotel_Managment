from flask import render_template, url_for, flash, redirect, request
from hotelmanagment import app, db, bcrypt
from hotelmanagment.forms import HotelForm, RegistrationForm, LoginForm
from hotelmanagment.models import User, Booking
from flask_login import login_user, current_user, logout_user, login_required


adminEmail = 'hotelmanagment213@gmail.com'
adminPassword = 'AdminView'

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
        if form.email.data == adminEmail and form.password.data == adminPassword: #Checks if the login user is the admin user.
            login_user(user, remember = form.remember.data)
            flash(f"Greetings Hotel Palm Aire Manager!\n Here is your list of clients currently reserved for rooms.")
            return redirect(url_for('admin_view'))
        elif user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('client_view')) 
        flash(f'Login Unsuccessful. Please check username and password', 'danger') 
    return render_template('login.html', title='Login', form=form) 

#Page where the user inputs their information about the stay.
@app.route("/hotel_form", methods=['GET', 'POST'])
def hotel_form():
    form = HotelForm()
    if form.validate_on_submit():
        booking = Booking(party_name = form.party_name.data, number_of_nights = form.number_of_nights.data, room_type = form.room_type.data, user_id = current_user.id)
        db.session.add(booking)
        db.session.commit()
        flash(f'Your booking information has been saved. Enjoy your stay', 'success')
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
@login_required
def admin_view():
    bookings = Booking.query.all()
    return render_template('admin_view.html', title='Admin View', bookings=bookings)

@app.route("/client_view")
@login_required
def client_view():
    bookings = Booking.query.filter_by(user_id = current_user.id)
    return render_template('client_view.html', title='Client View', bookings=bookings)

@app.route("/delete")
@login_required
def delete():
    bookings = Booking.query.filter_by(user_id = current_user.id).delete()
    #After fixing the iterable error above for the current_user.id we then need way of deleting rom client_view table after deleting from the Bookings Database
    return render_template('client_view.html', title ='Client View', bookings = bookings)

    
