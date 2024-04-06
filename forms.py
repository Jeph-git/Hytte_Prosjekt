from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField, DateField, ValidationError
from wtforms.validators import DataRequired, Length, Email
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    phoneNumber = StringField('Telefonnummer', validators=[DataRequired()], render_kw={"type": "tel"})
    password = PasswordField('Passord', validators=[DataRequired()])
    remember_me = BooleanField('Husk meg')  # New field for "Remember Me" checkbox
    submit = SubmitField('Logg inn')

class RegisterForm(FlaskForm):
    phoneNumber = StringField('Telefonnummer', validators=[DataRequired()], render_kw={"type": "tel"})
    password = PasswordField('Passord', validators=[DataRequired()])
    confirmPassword = PasswordField('Bekreft Passord', validators=[DataRequired()])
    submit = SubmitField('Registrer')

class CalendarForm(FlaskForm):
    ankomst = DateField('Ankomst Dato', format='%Y-%m-%d', validators=[DataRequired()])
    avreise = DateField('Avreise Dato', format='%Y-%m-%d', validators=[DataRequired()])
    melding = StringField('Skriv melding', widget=TextArea(), validators=[Length(max=255)])
    submit = SubmitField('Bestill')


class AddEmailForm(FlaskForm):
    email = StringField('E-postadresse', validators=[DataRequired(), Email()])
    submit = SubmitField('Legg til e-post')
