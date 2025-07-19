from app.models import User
from flask_wtf import FlaskForm
# from sqlalchemy.engine import URL
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, URL, Regexp
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


class EditTabForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired()])
    song = StringField('Song', validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[
        ('', 'Select difficulty'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'), 
        ('any', 'Any'),
    ])
    genre = StringField('Genre')
    harp_type = SelectField('Harp Type', choices=[
        ('Any', 'Any'),
        ('Chromatic', 'Chromatic'),
        ('Diatonic', 'Diatonic'),
        ('Melody Maker', 'Melody Maker'),
        ('Octave', 'Octave'),
        ('Tremolo', 'Tremolo')
    ], validators=[DataRequired()])
    harp_key = SelectField('Key', choices=[
        ('A', 'A'),
        ('A#/Bb', 'A#/Bb'),
        ('B','B'),
        ('C','C'), 
        ('C#/Db', 'C#/Db'), 
        ('D','D'),
        ('D#/Eb', 'D#/Eb'), 
        ('E', 'E'), 
        ('F', 'F'), 
        ('F#/Gb', 'F#/Gb'), 
        ('G', 'G'), 
        ('G#/Ab', 'G#/Ab'), 
        ('Any', 'Any'),
        ('Unknown', 'Unknown')
    ], validators=[DataRequired()])
    content = TextAreaField('Tab Content', validators=[DataRequired()])
    youtube_link = StringField('YouTube Link')
    submit = SubmitField('Update Tab')

class AddTabForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired(), Length(max=200)])
    song = StringField('Song Title', validators=[DataRequired(), Length(max=200)])
    difficulty = SelectField('Difficulty', choices=[
        ('', 'Select difficulty'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'), 
        ('any', 'Any'),
    ], validators=[Optional()])
    genre = StringField('Genre', validators=[Optional(), Length(max=100)])
    harp_type = SelectField('Harp Type', choices=[
        ('Any', 'Any'),
        ('Chromatic', 'Chromatic'),
        ('Diatonic', 'Diatonic'),
        ('Melody Maker', 'Melody Maker'),
        ('Octave', 'Octave'),
        ('Tremolo', 'Tremolo')
    ], validators=[DataRequired()])
    harp_key = SelectField('Harp Key', choices=[
        ('A', 'A'),
        ('A#/Bb', 'A#/Bb'),
        ('B','B'),
        ('C','C'), 
        ('C#/Db', 'C#/Db'), 
        ('D','D'),
        ('D#/Eb', 'D#/Eb'), 
        ('E', 'E'), 
        ('F', 'F'), 
        ('F#/Gb', 'F#/Gb'), 
        ('G', 'G'), 
        ('G#/Ab', 'G#/Ab'), 
        ('Any', 'Any'),
        ('Unknown', 'Unknown')
    ], validators=[DataRequired()])
    content = TextAreaField('Tab Content', validators=[DataRequired()])
    youtube_link = StringField('YouTube Link', validators=[
        Optional(), 
        URL(message='Please enter a valid URL'),
        Regexp(r'(youtube\.com|youtu\.be)', message='Must be a YouTube URL')
    ])
    submit = SubmitField('Add Tab')









    
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