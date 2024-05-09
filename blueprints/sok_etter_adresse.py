from database import db
from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash, jsonify
from forms import AddressForm
from flask_login import login_required, current_user
import urllib.parse
import requests
from models import Address
from utils import role_required, ROLES

SOK_ADRESSE = Blueprint('sok_adresse', __name__)

@SOK_ADRESSE.route('/search', methods=['GET'])
@login_required
def search_address():
    query = request.args.get('query', '')
    formatted_query = urllib.parse.quote(query.lower())
    URL = f'https://ws.geonorge.no/adresser/v1/sok?adressetekst={formatted_query}'
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        addresses = []
        for address in data.get('adresser', []):
            address_info = {
                'full_address': address['adressetekst'],
                'postnummer': address.get('postnummer', ''),
                'poststed': address.get('poststed', ''),
                'latitude': address.get('representasjonspunkt', {}).get('lat', ''),
                'longitude': address.get('representasjonspunkt', {}).get('lon', '')
            }
            addresses.append(address_info)
        return jsonify(addresses)
    else:
        return jsonify([])
