from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_user
from flask_login import login_required
from flask_login import current_user

from database import db

from models import User
from models import Customer
from models import User_Customer
from models import Governor_User
from models import Address

from forms import RegisterForm
from forms import RegisterGovernorForm
from forms import RegisterCustomer
from forms import RegisterUserForm
from forms import RegisterPlowmanForm

from utils import generate_token
from utils import send_token



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

@login_required
@REGISTER.route('/register_governor', methods=['POST', 'GET'])
def register_governor():
    title='Registrer Ordfører'
    form = RegisterGovernorForm()
    # Retrieve all customers
    customers = Customer.query.all()
    form.customer.choices = [(customer.id, customer.name) for customer in customers]

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

                # Retrieve the selected customer ID from the form
                selected_customer_id = form.customer.data

                # Create a relationship between the user and the selected customer
                user_customer = User_Customer(
                    user_id=new_user.id,
                    customer_id=selected_customer_id
                )
                db.session.add(user_customer)
                db.session.commit()
                token = generate_token(new_user.id)
                password_set_url = send_token(new_user, token)
                flash(f'Ordfører registrert. Oppsett av passord er sendt til TLF.\nSett passord <a href="/{password_set_url}" class="alert-link">her</a>', 'success')
                # flash('Ordfører registrert.', 'success')
                return redirect(url_for('register.register_governor'))
        else:
            flash('Vennligst skriv inn et gyldig telefonnummer.', 'danger')
    return render_template('register_governor.html', form=form, title=title, role='ordfører')

@login_required
@REGISTER.route('/register_user', methods=['POST', 'GET'])
def register_user():
    title = 'Registrer Bruker'
    form = RegisterUserForm()
    
    if form.validate_on_submit():
        if form.phoneNumber.data.isdigit() and len(form.phoneNumber.data) >= 8:
            user = User.query.filter_by(phoneNumber=form.phoneNumber.data).first()
            if user:
                flash('Telefonnummeret er allerede registrert.', 'danger')
            else:
                # Check if email is already registered
                email_user = User.query.filter_by(email=form.email.data).first()
                if email_user:
                    flash('Email is already registered.', 'danger')
                    return redirect(url_for('register.register_user'))
                else:
                    address = form.addressText.data
                    zip_code = form.zipCode.data
                    postplace = form.postPlace.data
                    latitude = form.latitude.data
                    longitude = form.longitude.data
                    
           
                    # Legger til ny bruker
                    new_user = User(phoneNumber=form.phoneNumber.data)
                    new_user.add_email(form.email.data)
                    new_user.role = 'cabin_owner'
                    db.session.add(new_user)
                    # db.session.commit()

                    # Hent kunden tilknyttet formannen (governor)
                    governor_customer_id = User_Customer.query.filter_by(user_id=current_user.id).first().customer_id

                    # Legger til "link" mellom formann og bruker
                    governor_user = Governor_User(
                        governor_id=current_user.id,
                        user_id=new_user.id
                    )
                    db.session.add(governor_user)
                    
                    # Gi brukeren samme kunde som formann   
                    user_customer = User_Customer(
                        user_id=new_user.id,
                        customer_id=governor_customer_id
                    )

                    db.session.add(user_customer)

                    # db.session.commit()
                    new_address = Address(
                        address=address,
                        postnummer=zip_code,
                        poststed=postplace,
                        latitude=latitude,
                        longitude=longitude,
                        user_id=new_user.id
                    )

                    db.session.add(new_address)
                    db.session.commit()

                    # Generer token
                    token = generate_token(new_user.id)
                    password_set_url = send_token(new_user, token)
           
                    flash(f'Hytteeier registrert. Oppsett av passord er sendt til TLF.\nSett passord <a href="/{password_set_url}" class="alert-link">her</a>', 'success')
                    return redirect(url_for('register.register_user'))
        else:
            flash('Vennligst skriv inn et gyldig telefonnummer.', 'danger')
    return render_template('register_users.html', form=form, title=title, role='user', active_page = 'register_user')




@login_required
@REGISTER.route('/register_customer', methods=['POST', 'GET'])
def register_customer():
    title = 'Registrer Kunde'
    form = RegisterCustomer()
    if form.validate_on_submit():
        new_customer = Customer(name=form.name.data)
        db.session.add(new_customer)
        db.session.commit()

        flash('Kunde registrert.', 'success')
        return redirect(url_for('register.register_customer'))


    return render_template('register_customer.html', form=form, title=title)


@login_required
@REGISTER.route('/register_plowman', methods=['POST', 'GET'])
def register_plowman():
    title = 'Registrer Plowman'
    form = RegisterPlowmanForm()
    customers = Customer.query.all()
    form.customer.choices = [(customer.id, customer.name) for customer in customers]

    if form.validate_on_submit():
        if form.phoneNumber.data.isdigit() and len(form.phoneNumber.data) >= 8:
            user = User.query.filter_by(phoneNumber=form.phoneNumber.data).first()
            if user:
                flash('Telefonnummeret er allerede registrert.', 'danger')
            else:
                new_user = User(phoneNumber=form.phoneNumber.data)
                new_user.add_email(form.email.data)
                new_user.role = 'plowman'
                db.session.add(new_user)
                db.session.commit()

                token = generate_token(new_user.id)
                send_token(new_user, token)
                
                selected_customer_ids = form.customer.data

                for customer_id in selected_customer_ids:
                    print(customer_id)
                    user_customer = User_Customer(
                        user_id=new_user.id,
                        customer_id=customer_id
                    )
                    db.session.add(user_customer)

                db.session.commit()
                                    # Generer token
                token = generate_token(new_user.id)
                password_set_url = send_token(new_user, token)
           
                flash(f'Plowman registrert. Oppsett av passord er sendt til TLF.\nSett passord <a href="/{password_set_url}" class="alert-link">her</a>', 'success')
                # flash('Plowman registrert.', 'success')
                return redirect(url_for('register.register_plowman'))

        else:
            flash('Vennligst skriv inn et gyldig telefonnummer.', 'danger')
    return render_template('register_plowman.html', form=form, title=title, role='plowman')
