from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, Optional
from flask_wtf.file import FileField, FileAllowed


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    profile_picture = FileField(
        'Profile Picture',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only images are allowed!')])
    new_password = PasswordField('New Password', validators=[Length(min=6, max=20), Optional(), Regexp(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])[\w!@#$%^&*()\-_=+{}\[\]:;,.?]{6,20}$',
        message='Password must be 6–20 characters long, contain at least one lowercase letter, one uppercase letter, and one special character. Spaces and disallowed characters are not allowed.'
    )])
    confirm_new_password = PasswordField('Confirm New Password', validators=[EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Edit')
