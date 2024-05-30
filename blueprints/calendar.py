from flask import Flask, Blueprint, session, redirect, url_for, render_template, request, jsonify
from flask_login import login_required, logout_user, current_user
from models import Bestilling, User, Address, User_Customer, Customer
from weather import get_weather
from utils import role_required, ROLES
from forms import SelectCustomer



CALENDAR = Blueprint('calendar', __name__)

@CALENDAR.route('/calendar', methods=['GET', 'POST'])
@role_required(ROLES[3])
@login_required
def display_calendar():
    title = 'Kalender'
    customer_count = len(User_Customer.query.filter_by(user_id=current_user.id).all())
    
    form = SelectCustomer()


    
    user_customers = User_Customer.query.filter(User_Customer.user_id != current_user.id).all()

    
    customer_ids = [user_customer.customer_id for user_customer in user_customers]

    
    customers = Customer.query.join(User_Customer).filter(User_Customer.user_id == current_user.id).all()

    
    customers = [customer for customer in customers if customer.id in customer_ids]

    
    form.customer.choices = [(customer.id, customer.name) for customer in customers]

    if form.validate_on_submit():
        selected_customer_id = form.customer.data
        session['selected_customer_id'] = selected_customer_id
        print(f"Selected Customer ID {session.get('selected_customer_id')}")
    else:
        print(f"Selected Customer ID {session.get('selected_customer_id')}")
        selected_customer_id = session.get('selected_customer_id')
        
        if not selected_customer_id and customers:
            selected_customer_id = customers[0].id

    form.customer.data = selected_customer_id

    events = []
    if selected_customer_id:

        user_ids = [uc.user_id for uc in User_Customer.query.filter_by(customer_id=selected_customer_id).all()]

        orders = Bestilling.query.filter(Bestilling.bestillings_id.in_(user_ids), Bestilling.order_pending == True).all()
        
        for order in orders:
            user = User.query.get(order.bestillings_id)
            if user:
                address = Address.query.filter_by(user_id=user.id).first()
                if address:
                    events.append({
                        'title': f'Hytteeier {user.id}',
                        'start': order.ankomst.strftime('%Y-%m-%d'),
                        'end': order.avreise.strftime('%Y-%m-%d'),
                        'userId': user.id,
                        'message': order.melding,
                        'address': address.address,
                        'postnummer': address.postnummer,
                        'poststed': address.poststed,
                        'latitude': address.latitude,
                        'longitude': address.longitude,
                    })

    for event in events:
        if event['message']:
            event['message'] = event['message'].replace('\r\n', '')
        
    return render_template('calendar.html', events=events, active_page='calendar', title=title, form=form)

    







@CALENDAR.route('/weather/<date>')
@login_required
def get_weather_for_date(date):
    city = 'Bergen'
    print(date)
    weather_icon = get_weather(city, date)  
    return jsonify({'weather_icon': weather_icon})