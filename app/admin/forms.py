from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    role = SelectField('Role', 
                      choices=[('admin', 'Admin'), ('editor', 'Editor'), ('viewer', 'Viewer')],
                      validators=[DataRequired()])
    submit = SubmitField('Update User')