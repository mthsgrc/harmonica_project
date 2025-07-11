from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.validators import ValidationError
from app.models import User
import re

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

########   Add to RegistrationForm class  #######
########  Add Password Strength Validation (Optional)   #######

# def validate_password(self, password):
#     # At least one digit
#     if not re.search(r"\d", password.data):
#         raise ValidationError('Password must contain at least one digit')
#     # At least one uppercase letter
#     if not re.search(r"[A-Z]", password.data):
#         raise ValidationError('Password must contain at least one uppercase letter')
#     # At least one special character
#     if not re.search(r"[ !@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password.data):
#         raise ValidationError('Password must contain at least one special character') 