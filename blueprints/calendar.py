from flask import Flask, Blueprint, session, redirect, url_for, render_template, request, jsonify
from flask_login import login_required, logout_user, current_user
from models import Bestilling, User, Address, User_Customer, Customer
from weather import get_weather
from utils import role_required, ROLES
from forms import SelectCustomer
'''
[{'title': 'Hytteeier 124', 'start': '2024-04-25', 'end': '2024-04-26', 'userId': 124, 'message': '22 Test - KUNDE: GEILO', 'address': 'Slottsplassen 1', 'postnummer': '0010', 'poststed': 'OSLO'}, 
{'title': 'Hytteeier 126', 'start': '2024-04-26', 'end': '2024-04-27', 'userId': 126, 'message': 'KUNDE:; HEMSEDAL\r\n', 'address': 'Tåsenveien 131B', 'postnummer': '0880', 'poststed': 'OSLO'}, 
{'title': 'Hytteeier 126', 'start': '2024-04-26', 'end': '2024-05-05', 'userId': 126, 'message': 'azfazxfa', 'address': 'Tåsenveien 131B', 'postnummer': '0880', 'poststed': 'OSLO'}]

'''


CALENDAR = Blueprint('calendar', __name__)

@CALENDAR.route('/calendar', methods=['GET', 'POST'])
@role_required(ROLES[3])
@login_required
def display_calendar():
    title = 'Kalender'
    customer_count = len(User_Customer.query.filter_by(user_id=current_user.id).all())
    
    selected_customer_id = None
    if customer_count > 0:

        selected_customer_id = User_Customer.query.filter_by(user_id=current_user.id).first().customer_id
    
    events = []
    form = SelectCustomer()
    customers = Customer.query.join(User_Customer).filter(User_Customer.user_id == current_user.id).all()
    form.customer.choices = [(customer.id, customer.name) for customer in customers]

    if form.validate_on_submit():
        selected_customer_id = form.customer.data

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
                    })

    for event in events:
        event['message'] = event['message'].replace('\r\n', '')
        
    return render_template('calendar.html', events=events, active_page='calendar', title=title, form=form)

    







@CALENDAR.route('/weather/<date>')
@login_required
def get_weather_for_date(date):
    city = 'Bergen'
    print(date)
    weather_icon = get_weather(city, date)  
    return jsonify({'weather_icon': weather_icon})