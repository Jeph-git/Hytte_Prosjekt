from flask import Flask, Blueprint, session, redirect, url_for, render_template, flash
from models import User, Bestilling
from flask_login import current_user, login_required
from database import db


ORDERS = Blueprint('orders', __name__)


@ORDERS.route('/orders')
@login_required
def orders():
    title = 'Bestillinger - Brøyting.net'
    # Query the database to retrieve the orders for the current user
    user_orders = Bestilling.query.filter_by(bestillings_id=current_user.id).all()
    
    # Render the template with the orders data
    return render_template('orders_html.html', user_orders=user_orders, title=title, active_page='orders')

@ORDERS.route('/orders/delete/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    order = Bestilling.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        flash('Order deleted successfully', 'success')
    else:
        flash('Failed to delete order. Order not found.', 'danger')
    return redirect(url_for('orders.orders'))