from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    usertype = RadioField('Label', choices=[('0', 'customer'), ('1', 'costume rental shop')], default='0', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password1', validators=[DataRequired()])
    password2 = PasswordField('Password2', validators=[DataRequired()])
    # usertype = RadioField('Label', choices=[('0', 'customer'), ('1', 'barbershop')], default='0', validators=[DataRequired()])
    submit = SubmitField('Sign Up')