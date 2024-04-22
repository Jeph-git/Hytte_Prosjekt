from flask import Flask, Blueprint, session, redirect, url_for, render_template
from flask_login import login_required, logout_user
from models import Bestilling

CALENDAR = Blueprint('calendar', __name__)

@CALENDAR.route('/calendar')
@login_required
def display_calendar():
    title = 'Kalender'
    orders = Bestilling.query.filter_by(order_pending=True).all()
    events = []
    for order in orders:
        events.append({
            'title': f'Hytteeier {order.bestillings_id}',
            'start': order.ankomst.strftime('%Y-%m-%d'),
        })
    return render_template('calendar.html', events=events, active_page='calendar', title=title)