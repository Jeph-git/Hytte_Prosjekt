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

    # Get all User_Customer records excluding the current user
    user_customers = User_Customer.query.filter(User_Customer.user_id != current_user.id).all()

    # Get all customer IDs from the User_Customer records
    customer_ids = [user_customer.customer_id for user_customer in user_customers]

    # Get all customers that are linked to the current user
    customers = Customer.query.join(User_Customer).filter(User_Customer.user_id == current_user.id).all()

    # Filter out customers that are only linked to the current user
    customers = [customer for customer in customers if customer.id in customer_ids]

    # Update the form choices
    form.customer.choices = [(customer.id, customer.name) for customer in customers]

    # If form has been submitted
    if form.validate_on_submit():
        # Set the selected customer in the form to the submitted value
        selected_customer_id = form.customer.data
        # Store the selected customer in the session
        session['selected_customer_id'] = selected_customer_id
    else:
        # If the form has not been submitted or if there was a validation error,
        # try to get the selected customer from the session
        print(session.get('selected_customer_id'))
        selected_customer_id = session.get('selected_customer_id')
        # If there is no value stored in the session, default to the first customer in the choices
        if not selected_customer_id and customers:
            selected_customer_id = customers[0].id

    # Set the selected customer in the form
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
        })
    print(order_pending_list)
    
    with open('map/config_kvam.json', encoding='utf-8') as config_file:
        config_data = json.load(config_file)

    return render_template('map.html', markers=markers, active_page='map', title=title, form=form)
