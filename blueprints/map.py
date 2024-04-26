from flask import Flask, url_for, render_template, request, session, redirect, Blueprint
from database import db
from datetime import datetime
import json
from flask_login import login_required, current_user
from models import Address, User, Bestilling
from utils import role_required, ROLES

MAP = Blueprint('map', __name__)

@MAP.route('/map', methods=['POST', 'GET'])
@role_required(ROLES[3])
@login_required
def map():
    title = 'Kart - Brøyting.net'
    addresses = Address.query.all()
   
    markers = []
    for address in addresses:
        order_pending_list = []
        user = User.query.get(address.user_id)
        if user:
            for bestilling in user.bestillinger:

                order_pending_list.append(bestilling.order_pending)

        markers.append({
            'adressetekst': address.address,
            'poststed': address.poststed,
            'postnummer': address.postnummer,
            'representasjonspunkt': {
                'lat': address.latitude,
                'lon': address.longitude
            },
            'order_pending': order_pending_list  
        })

    with open('map/config_kvam.json', encoding='utf-8') as config_file:
        config_data = json.load(config_file)

    return render_template('map.html', config=config_data, markers=markers, active_page='map', title=title)
