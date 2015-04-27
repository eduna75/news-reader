from flask.ext.wtf import Form, RecaptchaField
from wtforms import BooleanField, TextField, PasswordField, SelectField
from wtforms.validators import Required, Email, EqualTo
from app.login.models import Feed


class LoginForm(Form):
    email = TextField('Email Address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    logged_in = BooleanField('Stay logged in', default='n')


class RegistrationForm(Form):
    name = TextField('Username', [Required()])
    email = TextField('Email Address', [Required(), Email()])
    password = PasswordField('New Password', [Required()])
    confirm = PasswordField('Repeat Password', [EqualTo('confirm', message='Passwords must match')])
    accept_tos = BooleanField('I accept the TOS', [Required()])
    captcha = RecaptchaField('Recaptcha')