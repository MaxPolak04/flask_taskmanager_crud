from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, EmailField, PasswordField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo, Regexp


class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20), Regexp(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])[\w!@#$%^&*()\-_=+{}\[\]:;,.?]{6,20}$',
        message='Password must be 6–20 characters long, contain at least one lowercase letter, one uppercase letter, and one special character. Spaces and disallowed characters are not allowed.'
    )])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    is_admin = BooleanField('Is Admin', default=False, validators=[Optional()])


class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    profile_picture = FileField(
        'Profile Picture',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only images are allowed!')])
    password = PasswordField('Password', validators=[Optional(), Length(min=6, max=20), Regexp(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])[\w!@#$%^&*()\-_=+{}\[\]:;,.?]{6,20}$',
        message='Password must be 6–20 characters long, contain at least one lowercase letter, one uppercase letter, and one special character. Spaces and disallowed characters are not allowed.'
    )])
    confirm_password = PasswordField('Confirm Password', validators=[Optional(), EqualTo('password', message='Passwords must match')])
    is_admin = BooleanField('Is Admin', default=False, validators=[Optional()])


class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete User')
