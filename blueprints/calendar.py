from flask import Flask, Blueprint, session, redirect, url_for, render_template
from flask_login import login_required, logout_user
from utils import role_required
from models import Bestilling, User, Address
from weather import get_weather


CALENDAR = Blueprint('calendar', __name__)

@CALENDAR.route('/calendar')
@role_required('plowman')
@login_required
def display_calendar():
    title = 'Kalender'
    orders = Bestilling.query.filter_by(order_pending=True).all()
    events = []
    for order in orders:
        # Query the user associated with the order
        user = User.query.get(order.bestillings_id)
        if user:
            # Query the address associated with the user
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
    return render_template('calendar.html', events=events, active_page='calendar', title=title)


from flask import jsonify

# Assume get_weather function is imported from weather.py

@CALENDAR.route('/weather/<date>')
@login_required
def get_weather_for_date(date):
    # Call the get_weather function from weather.py passing the city and date
    # Replace 'Bergen' with your desired location
    city = 'Bergen'
    print(date)
    weather_icon = get_weather(city, date)  # Pass both city and date to get_weather
    return jsonify({'weather_icon': weather_icon})