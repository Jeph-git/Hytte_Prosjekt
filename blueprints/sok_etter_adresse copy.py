from flask import Flask, Blueprint, request, render_template
from flask_login import login_required
import urllib.parse
import requests


SOK_ADRESSE = Blueprint('sok_adresse', __name__)

@SOK_ADRESSE.route('/sok_adresse')
@login_required
def sok_adresse():
    return render_template('sok_adresse.html')

@SOK_ADRESSE.route('/process_address', methods=['POST'])
def process_address():
    selected_address = request.json
    # Now you have the selected address object in Python
    print('Selected Address:', selected_address)
    # Process the address further as needed
    return 'Address received successfully.', 200


@SOK_ADRESSE.route('/search', methods=['GET'])
@login_required
def search_address():
    query = request.args.get('query')

    formatted_query = urllib.parse.quote(query.lower())
    URL = f'https://ws.geonorge.no/adresser/v1/sok?adressetekst={formatted_query}'
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        addresses = data['adresser']
        print(addresses)
        return addresses
    else:
        return {'error': 'Feil ved søk'}, 500
