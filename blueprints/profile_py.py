from flask import url_for
from flask import render_template
from flask import redirect
from flask import Blueprint
from flask import flash

from babel.dates import format_datetime

from flask_babel import _

from models import User

from forms import AddEmailForm

from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required

from database import db




PROFIL = Blueprint('profil', __name__)

@PROFIL.route('/profil', methods=['POST', 'GET'])
@login_required
def profil():
    title = 'Profil - Brøyting.net'
    tlfnummer = current_user.phoneNumber
    user = User.query.filter_by(phoneNumber=tlfnummer).first()  
    email = user.email
    date_added = user.date_added   
    formatted_date_added = format_datetime(date_added, "d. MMMM yyyy", locale='nb_NO') 
    return render_template('profil_html.html', title=title, tlfnummer=tlfnummer, date_added=formatted_date_added, active_page='profil', rediger_profil=False, email=email)


@PROFIL.route('/profil/rediger', methods=['GET', 'POST'])
@login_required
def rediger_profil():
    form = AddEmailForm()
    if form.validate_on_submit():
        new_email = form.email.data
        if new_email != current_user.email:
            
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user:
                flash('E-postadressen er allerede i bruk av en annen bruker. Vennligst velg en annen e-postadresse.', 'error')
            else:
                
                current_user.email = new_email
                db.session.commit()
                flash('Profilen din ble oppdatert.', 'success')
        
    title = 'Rediger Profil - Brøyting.net'
    email = current_user.email
    return render_template('rediger_profil.html', title=title, form=form, email=email)

@PROFIL.route('/profil/slett', methods=['POST'])
@login_required
def slett_profil():
    
    current_user.delete_account()
    flash('Kontoen din ble slettet.', 'success')
    logout_user() 
    return redirect(url_for('login.login'))