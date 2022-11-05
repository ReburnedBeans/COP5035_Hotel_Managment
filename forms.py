from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#Class: HotelForm
#Functionality: Allows user to upload their room type and number of nights to the DB.
class HotelForm(FlaskForm):
    name = StringField('Name of Party',
                           validators=[DataRequired(), Length(min=2, max=20)])
    room_type = IntegerField('Room Type', validators=[DataRequired(), NumberRange(1,5)])
    number_of_nights = IntegerField('Expected Number of Nights Staying', validators=[DataRequired()])
    submit = SubmitField('Submit')