from flask import Flask, url_for, render_template, request, session, redirect, Blueprint
from database import db
from datetime import datetime
import json
from flask_login import login_required, current_user
from models import Address, User, Bestilling, User_Customer, Customer
from utils import role_required, ROLES
from forms import SelectCustomer

MAP = Blueprint('map', __name__)

from flask import session

@MAP.route('/map', methods=['POST', 'GET'])
@role_required(ROLES[3])
@login_required
def map():
    title = 'Kart - Brøyting.net'
    form = SelectCustomer()

    

    user_customers = User_Customer.query.filter(User_Customer.user_id != current_user.id).all()

    customer_ids = [user_customer.customer_id for user_customer in user_customers]

    customers = Customer.query.join(User_Customer).filter(User_Customer.user_id == current_user.id).all()

    customers = [customer for customer in customers if customer.id in customer_ids]

    form.customer.choices = [(customer.id, customer.name) for customer in customers]

    if form.validate_on_submit():

        selected_customer_id = form.customer.data

        session['selected_customer_id'] = selected_customer_id
    else:


        print(session.get('selected_customer_id'))
        selected_customer_id = session.get('selected_customer_id')

        if not selected_customer_id and customers:
            selected_customer_id = customers[0].id

    form.customer.data = selected_customer_id

    user_ids = []
    if selected_customer_id:
        user_ids = [uc.user_id for uc in User_Customer.query.filter_by(customer_id=selected_customer_id).all()]

    addresses = Address.query.filter(Address.user_id.in_(user_ids)).all()



    markers = []
    for address in addresses:
        order_pending_list = []
        order_messages = []
        user = User.query.get(address.user_id)
        if user:
            # Get phonenumber
            phone = user.phoneNumber
            for bestilling in user.bestillinger:
                message = bestilling.melding
                order_messages.append(message) 
                order_pending_list.append(bestilling.order_pending)
            
                has_message = len(message) > 0 if message is not None else False

        markers.append({
            'adressetekst': address.address,
            'poststed': address.poststed,
            'postnummer': address.postnummer,
            'representasjonspunkt': {
                'lat': address.latitude,
                'lon': address.longitude
            },
            'order_pending': order_pending_list ,
            'message' : order_messages,
            'hasMessage': has_message,
            'phone': phone,
        })
    print(order_pending_list)

    with open('map/config_kvam.json', encoding='utf-8') as config_file:
        config_data = json.load(config_file)

    return render_template('map.html', markers=markers, active_page='map', title=title, form=form)
