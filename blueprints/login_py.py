from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models import User
from forms import LoginForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

LOGIN = Blueprint('login', __name__)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def initialize_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'  
    return login_manager

# Feilmelding for når man ikke er logget inn
@login_manager.unauthorized_handler
def unauthorized():
    flash('Vennligst logg inn', 'warning')
    return redirect(url_for('login.login'))



@LOGIN.route('/login', methods=['GET', 'POST'])
def login():
    title='Login - Brøyting.net'
    form = LoginForm()


    phoneNumber = request.args.get('phoneNumber', '')


    # Fyller ut telefonnummerfeltet hvis det eksisterer
    if phoneNumber:
        form.phoneNumber.data = phoneNumber
    
    if form.validate_on_submit():
        if form.phoneNumber.data.isdigit() and len(form.phoneNumber.data) >= 8:
            user = User.query.filter_by(phoneNumber=form.phoneNumber.data).first()
            if user:
                if user.password_hash:
                    if user.check_password(form.password.data):
                        remember = form.remember_me.data  # Sjekk om brukeren vil bli husket
                        print(remember)
                        session.clear()
                        login_user(user, remember=remember)
                        '''
                        # check_role = current_user.role # Sjekk rollen, også redirect basert på det
                        # if role == 'admin':
                        '''
                        # flash('Logg inn vellykket')
                        return redirect(url_for('dashboard.dashboard'))
                    else:
                        flash('Feil passord', 'danger')
                else:
                    flash('Du må sette opp passord', 'danger') 
            else:
                flash('Ingen konto registrert med dette telefonnummeret', 'danger')
        else:
            flash('Vennligst skriv inn et gyldig telefonnummer.', 'danger')
    return render_template('login_html.html', form=form, title=title)
