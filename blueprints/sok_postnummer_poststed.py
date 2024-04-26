import requests
from models import AddressTesting
from database import db
from utils import timeit
from flask import Blueprint, render_template, redirect, url_for
from forms import AddressFormTESTING

POSTNUMMER_TESTING = Blueprint('testing', __name__)

@POSTNUMMER_TESTING.route('/testing', methods=['GET', 'POST'])
def fetch_addresses():
    form = AddressFormTESTING()
    if form.validate_on_submit():
        poststed = form.poststed.data
        postnummer = form.postnummer.data
        fetch_addresses_from_api(poststed, postnummer)
        return redirect(url_for('some_success_route')) 
    return render_template('adress_formTESTING.html', form=form)

@timeit
def fetch_addresses_from_api(poststed, postnummer):
    BASE_URL = 'https://ws.geonorge.no/adresser/v1/sok'
    page = 0

    while True:
        URL = f'{BASE_URL}?fuzzy=false&poststed={poststed}&postnummer={postnummer}&utkoordsys=4258&treffPerSide=10&side={page}&asciiKompatibel=true'
        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()
            addresses = data.get('adresser', [])

            if not addresses:
                break

            for address_data in addresses:
                if address_data.get('adressenavn'):
                    address = AddressTesting(
                        address=address_data.get('adressetekst'),
                        postnummer=address_data.get('postnummer'),
                        poststed=address_data.get('poststed'),
                        latitude=address_data.get('representasjonspunkt', {}).get('lat'),
                        longitude=address_data.get('representasjonspunkt', {}).get('lon'),
                        customer_name = 'Geilo'
                    )
                    db.session.add(address)
                    db.session.commit()

            page += 1
        else:
            print('Error fetching data')
            break
