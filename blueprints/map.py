from flask import Flask, url_for, render_template, request, session, redirect, Blueprint
from database import db
from datetime import datetime
import json
from flask_login import login_required
from models import Address

MAP = Blueprint('map', __name__)

@MAP.route('/map', methods=['POST', 'GET'])
@login_required
def map():
    title = 'Kart - Brøyting.net'
    session.pop('adresse', None)
    
    # Query addresses from the database
    addresses = Address.query.all()
    
    # Convert SQLAlchemy objects to dictionaries
    markers = [
        {
            'adressetekst': address.address,
            'poststed': address.poststed,
            'postnummer': address.postnummer,
            'representasjonspunkt': {
                'lat': address.latitude,
                'lon': address.longitude
            }
            # Add more fields as needed
        }
        for address in addresses
    ]
    
    # Load initial view from the config file
    with open('map/config_kvam.json', encoding='utf-8') as config_file:
        config_data = json.load(config_file)
    
    return render_template('map.html', config=config_data, markers=markers, active_page='map', title=title)