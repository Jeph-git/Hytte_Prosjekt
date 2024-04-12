from flask import Flask, url_for, render_template, request, session, redirect, Blueprint
from database import db
from datetime import datetime
import json
from flask_login import login_required
from models import Address, User, Bestilling

MAP = Blueprint('map', __name__)

@MAP.route('/map', methods=['POST', 'GET'])
@login_required
def map():
    title = 'Kart - Brøyting.net'

    # Query addresses from the database
    addresses = Address.query.all()

    # Convert SQLAlchemy objects to dictionaries
    markers = []
    for address in addresses:
        # Initialize list to store order_pending status for each bestilling associated with the user of the address
        order_pending_list = []

        # Fetch the user associated with the address
        user = User.query.get(address.user_id)

        # If user exists, fetch bestillinger associated with the user
        if user:
            for bestilling in user.bestillinger:
                # Append order_pending status of each bestilling to the list
                order_pending_list.append(bestilling.order_pending)

        # Add marker data along with order_pending status list to markers list
        markers.append({
            'adressetekst': address.address,
            'poststed': address.poststed,
            'postnummer': address.postnummer,
            'representasjonspunkt': {
                'lat': address.latitude,
                'lon': address.longitude
            },
            'order_pending': order_pending_list  # List of order_pending statuses for bestillinger associated with the user
        })

    # Load initial view from the config file
    with open('map/config_kvam.json', encoding='utf-8') as config_file:
        config_data = json.load(config_file)

    return render_template('map.html', config=config_data, markers=markers, active_page='map', title=title)
