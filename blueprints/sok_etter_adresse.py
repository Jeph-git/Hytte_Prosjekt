from database import db
from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
from forms import AddressForm
from flask_login import login_required, current_user
import urllib.parse
import requests
from models import Address
from utils import role_required, ROLES

SOK_ADRESSE = Blueprint('sok_adresse', __name__)

@SOK_ADRESSE.route('/sok_adresse')
@role_required(ROLES[1], ROLES[2])
@login_required
def sok_adresse():
    title = 'Legg til adresse'
    form = AddressForm()
    return render_template('sok_adresse.html', form=form, active_page='adresse', title=title)

@SOK_ADRESSE.route('/process_address')
def process_address():
    address_data = request.args.get('address_data')
    address_dict = eval(address_data) 
    adressetekstForm = address_dict.get('adressetekst')
    postnummerForm = address_dict.get('postnummer')
    poststedForm = address_dict.get('poststed')
    # Få tilgang til nøstede nøkler
    representasjonspunkt = address_dict.get('representasjonspunkt', {})
    lonForm = representasjonspunkt.get('lon')
    latForm = representasjonspunkt.get('lat')
    bruker_id = current_user.id
    if Address.query.filter_by(user_id=bruker_id).count() >= 1:
        flash('Oppdatert adresse', 'success')
        oppdater_adresse = Address.query.filter_by(user_id=bruker_id).first()
        oppdater_adresse.update_address(
            new_address=adressetekstForm,
            new_postnummer=postnummerForm,
            new_poststed=poststedForm,
            new_latitude=latForm,
            new_longitude=lonForm
        )
        return redirect(url_for('sok_adresse.sok_adresse'))
    else:
        new_address = Address(
            address=adressetekstForm,
            postnummer=postnummerForm,
            poststed=poststedForm,
            latitude=latForm,
            longitude=lonForm,
            user_id=bruker_id
        )
        db.session.add(new_address)
        db.session.commit()
        flash('Adresse lagt til', 'success')
        return redirect(url_for('sok_adresse.sok_adresse'))

@SOK_ADRESSE.route('/search', methods=['GET', 'POST'])
@login_required
def search_address():
    form = AddressForm()
    if form.validate_on_submit():
        query = form.query.data
        formatted_query = urllib.parse.quote(query.lower())
        URL = f'https://ws.geonorge.no/adresser/v1/sok?adressetekst={formatted_query}'
        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()
            addresses = data.get('adresser', [])
            if len(addresses) == 0:
                flash('Ingen treff', 'danger')
                return redirect(url_for('sok_adresse.sok_adresse'))
            else:
                return render_template('sok_adresse.html', addresses=addresses, form=form)
        else:
            print('jeg kjører')
            return render_template('sok_adresse.html', addresses=[], error='Feil ved søk', form=form)
    return redirect(url_for('sok_adresse.sok_adresse'))