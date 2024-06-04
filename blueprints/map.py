from flask import Flask, url_for, render_template, request, session, redirect, Blueprint
from database import db
from datetime import datetime
import json
from flask_login import login_required, current_user
from models import Address, User, Bestilling, User_Customer, Customer
from utils import role_required, ROLES
from forms import SelectCustomer, ChooseDatesOnMap

MAP = Blueprint('map', __name__)

from flask import session

@MAP.route('/map', methods=['POST', 'GET'])
@role_required(ROLES[3])
@login_required
def map():
    title = 'Kart - Brøyting.net'
    select_customer_form = SelectCustomer()
    choose_dates_on_map_form = ChooseDatesOnMap()

    user_customers = User_Customer.query.filter(User_Customer.user_id != current_user.id).all()
    customer_ids = [user_customer.customer_id for user_customer in user_customers]

    customers = Customer.query.join(User_Customer).filter(User_Customer.user_id == current_user.id).all()
    customers = [customer for customer in customers if customer.id in customer_ids]
    select_customer_form.customer.choices = [(customer.id, customer.name) for customer in customers]

    if select_customer_form.validate_on_submit():
        selected_customer_id = select_customer_form.customer.data
        session['selected_customer_id'] = selected_customer_id
    else:
        selected_customer_id = session.get('selected_customer_id')
        if not selected_customer_id and customers:
            selected_customer_id = customers[0].id
    select_customer_form.customer.data = selected_customer_id

    user_ids = []
    if selected_customer_id:
        user_ids = [uc.user_id for uc in User_Customer.query.filter_by(customer_id=selected_customer_id).all()]

    addresses = Address.query.filter(Address.user_id.in_(user_ids)).all()
    markers = []
    for address in addresses:
        orders = []
        user = User.query.get(address.user_id)
        if user:
            bestillinger = Bestilling.query.filter_by(bestillings_id=user.id).order_by(Bestilling.ankomst).all()
            for bestilling in bestillinger:
                orders.append({
                    'order_pending': bestilling.order_pending,
                    'message': bestilling.melding,
                    'arrival_date': bestilling.ankomst.strftime('%Y-%m-%d') if bestilling.ankomst else None,
                    'departure_date': bestilling.avreise.strftime('%Y-%m-%d') if bestilling.avreise else None
                })

        markers.append({
            'adressetekst': address.address,
            'poststed': address.poststed,
            'postnummer': address.postnummer,
            'representasjonspunkt': {
                'lat': address.latitude,
                'lon': address.longitude
            },
            'orders': orders,
            'phone': user.phoneNumber if user else None
        })

    # with open('map/config_kvam.json', encoding='utf-8') as config_file:
    #     config_data = json.load(config_file)

    if choose_dates_on_map_form.validate_on_submit():
        print('Clicked!')

    return render_template('map.html', markers=markers, active_page='map', title=title, form=select_customer_form, choose_dates_on_map_form=choose_dates_on_map_form)
