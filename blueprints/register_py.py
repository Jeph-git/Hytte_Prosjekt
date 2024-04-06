from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash  # Use secure password hashing
from database import db
from models import User
from forms import RegisterForm

REGISTER = Blueprint('register', __name__)

@REGISTER.route('/register', methods=['POST', 'GET'])
def register():
    title = 'Registrer - Brøyting.net'
    form = RegisterForm()
    if form.validate_on_submit():
        if form.phoneNumber.data.isdigit() and len(form.phoneNumber.data) >= 8:
            user = User.query.filter_by(phoneNumber=form.phoneNumber.data).first()
            if user:
                flash('Telefonnummeret er allerede registrert.')
            else:
                if form.password.data != form.confirmPassword.data:
                    flash('Passordene matcher ikke.')
                else:
                    new_user = User(phoneNumber=form.phoneNumber.data)
                    new_user.set_password(form.password.data)
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Vennligst skriv inn et gyldig telefonnummer.')
    return render_template('register_html.html', form=form, title=title)
