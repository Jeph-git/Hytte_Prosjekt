from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField, DateField, ValidationError, SelectField, SelectMultipleField, FieldList
from wtforms.validators import DataRequired, Length, Email
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    phoneNumber = StringField('Telefonnummer', validators=[DataRequired()], render_kw={"type": "tel"})
    # email = StringField('E-postadresse', validators=[DataRequired(), Email()])
    password = PasswordField('Passord', validators=[DataRequired()])
    remember_me = BooleanField('Husk meg')  
    submit = SubmitField('Logg inn')

class RegisterForm(FlaskForm):
    phoneNumber = StringField('Telefonnummer', validators=[DataRequired()], render_kw={"type": "tel"})
    email = StringField('E-postadresse', validators=[DataRequired(), Email()])
    password = PasswordField('Passord', validators=[DataRequired()])
    confirmPassword = PasswordField('Bekreft Passord', validators=[DataRequired()])
    submit = SubmitField('Registrer')

# Registrer ordfører 
class RegisterGovernorForm(FlaskForm):
    phoneNumber = StringField('Telefonnummer', validators=[DataRequired()], render_kw={"type": "tel"})
    email = StringField('E-postadresse', validators=[DataRequired(), Email()])
    customer = SelectField('Kunde', coerce=int)  
    submit = SubmitField('Registrer')

class RegisterPlowmanForm(FlaskForm):
    phoneNumber = StringField('Telefonnummer', validators=[DataRequired()], render_kw={"type": "tel"})
    email = StringField('E-postadresse', validators=[DataRequired(), Email()])
    customer = SelectMultipleField('Kunde', coerce=int)  
    # customer = FieldList(BooleanField('Kunde'), min_entries=1)  
    submit = SubmitField('Registrer')

class RegisterUserForm(FlaskForm):
    phoneNumber = StringField('Telefonnummer', validators=[DataRequired()], render_kw={"type": "tel"})
    email = StringField('E-postadresse', validators=[DataRequired(), Email()])
    poststed = StringField('Poststed', validators=[DataRequired()])
    postnummer = StringField('Postnummer', validators=[DataRequired()])
    submit = SubmitField('Registrer')

class RegisterCustomer(FlaskForm):
    name = StringField('navn')
    submit = SubmitField('Registrer')

class SetPasswordForm(FlaskForm):
    password = PasswordField('Passord', validators=[DataRequired()])
    confirmPassword = PasswordField('Bekreft Passord', validators=[DataRequired()])
    submit = SubmitField('Registrer')
    
class CalendarForm(FlaskForm):
    ankomst = DateField('Ankomst til hytten', format='%Y-%m-%d', validators=[DataRequired()])
    avreise = DateField('Avreise fra hytten', format='%Y-%m-%d', validators=[DataRequired()])
    melding = StringField('Skriv melding til brøyter', widget=TextArea(), validators=[Length(max=255)])
    submit = SubmitField('Bestill')


class AddEmailForm(FlaskForm):
    email = StringField('E-postadresse', validators=[DataRequired(), Email()])
    submit = SubmitField('Legg til e-post')

class AddressForm(FlaskForm):
    query = StringField('Adresse', validators=[DataRequired()], render_kw={"placeholder": "Skriv inn adresse"})
    submit = SubmitField('Søk')


class AddressFormTESTING(FlaskForm):
    poststed = StringField('Poststed', validators=[DataRequired()])
    postnummer = StringField('Postnummer', validators=[DataRequired()])
    submit = SubmitField('Fetch Addresses')



class SelectCustomer(FlaskForm):
    customer = SelectField('Kunde', coerce=int)  
    submit = SubmitField('Registrer')
