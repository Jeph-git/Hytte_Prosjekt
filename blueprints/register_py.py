from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash  # Use secure password hashing
from database import db
from models import User, Customer, User_Customer, Governor_User
from forms import RegisterForm, RegisterGovernorForm, RegisterCustomer
from utils import generate_token, send_token

REGISTER = Blueprint('register', __name__)

@REGISTER.route('/register', methods=['POST', 'GET'])
def register():
    title = 'Registrer - Brøyting.net'
    form = RegisterForm()
    if form.validate_on_submit():
        if form.phoneNumber.data.isdigit() and len(form.phoneNumber.data) >= 8:
            user = User.query.filter_by(phoneNumber=form.phoneNumber.data).first()
            if user:
                flash('Telefonnummeret er allerede registrert.', 'danger')
            else:
                if form.password.data != form.confirmPassword.data:
                    flash('Passordene matcher ikke.')
                else:
                    new_user = User(phoneNumber=form.phoneNumber.data)
                    new_user.set_password(form.password.data)
                    new_user.add_email(form.email.data)
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Vennligst skriv inn et gyldig telefonnummer.', 'danger')
    return render_template('register_html.html', form=form, title=title)

@REGISTER.route('/register_governor', methods=['POST', 'GET'])
def register_governor():
    title='Registrer Ordfører'
    form = RegisterGovernorForm()
    if form.validate_on_submit():
        if form.phoneNumber.data.isdigit() and len(form.phoneNumber.data) >= 8:
            user = User.query.filter_by(phoneNumber=form.phoneNumber.data).first()
            if user:
                flash('Telefonnummeret er allerede registrert.')
            else:
                new_user = User(phoneNumber=form.phoneNumber.data)
                new_user.add_email(form.email.data)
                new_user.role = 'governor'
                db.session.add(new_user)
                db.session.commit()

                # Generer token
                token = generate_token(new_user.id)

                # Send token til bruker
                send_token(new_user, token)
                
                flash('Ordfører registrert.', 'success')
                return redirect(url_for('register.register_governor'))
        else:
            flash('Vennligst skriv inn et gyldig telefonnummer.', 'danger')
    return render_template('register_users.html', form=form, title=title, role='ordfører')

@REGISTER.route('/register_user', methods=['POST', 'GET'])
def register_user():
    title = 'Registrer Bruker'
    form = RegisterGovernorForm()
    if form.validate_on_submit():
        if form.phoneNumber.data.isdigit() and len(form.phoneNumber.data) >= 8:
            user = User.query.filter_by(phoneNumber=form.phoneNumber.data).first()
            if user:
                flash('Telefonnummeret er allerede registrert.')
            else:
                new_user = User(phoneNumber=form.phoneNumber.data)
                new_user.add_email(form.email.data)
                new_user.role = 'cabin_owner'
                db.session.add(new_user)
                db.session.commit()

                governor_user = Governor_User(
                    governor_id = current_user.id,
                    user_id = new_user.id
                )
                db.session.add(governor_user)
                db.session.commit()

                # Generer token
                token = generate_token(new_user.id)

                # Send token til bruker
                send_token(new_user, token)

                flash('Hytteeier registrert.', 'success')
                return redirect(url_for('register.register_user'))
        else:
            flash('Vennligst skriv inn et gyldig telefonnummer.', 'danger')
    return render_template('register_users.html', form=form, title=title, role='user')


@REGISTER.route('/register_customer', methods=['POST', 'GET'])
def register_customer():
    title = 'Registrer Kunde'
    form = RegisterCustomer()
    if form.validate_on_submit():
        try:
            new_customer = Customer(name=form.name.data)
            db.session.add(new_customer)
            db.session.commit()


            user_customer = User_Customer(
                user_id=current_user.id, 
                customer_id=new_customer.id
                )
            db.session.add(user_customer)
            db.session.commit()


            flash('Kunde registrert.', 'success')
            return redirect(url_for('register.register_customer'))
        except:
            flash('Feil ved registrering av kunde', 'danger')
            return redirect(url_for('register.register_customer'))

    return render_template('register_customer.html', form=form, title=title)

