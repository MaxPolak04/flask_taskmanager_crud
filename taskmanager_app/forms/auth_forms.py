from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20), Regexp(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])[\w!@#$%^&*()\-_=+{}\[\]:;,.?]{6,20}$',
        message='Password must be 6–20 characters long, contain at least one lowercase letter, one uppercase letter, and one special character. Spaces and disallowed characters are not allowed.'
    )])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')


class SignInForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me signed in', default=False)
    submit = SubmitField('Sign In')
