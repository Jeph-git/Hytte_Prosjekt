from flask import Flask, Blueprint, session, redirect, url_for, render_template, flash, request
from models import User, Bestilling
from flask_login import current_user, login_required
from database import db


ORDERS = Blueprint('orders', __name__)


@ORDERS.route('/orders')
@login_required
def orders():
    title = 'Bestillinger - Brøyting.net'
    
    active_orders = Bestilling.query.filter_by(bestillings_id=current_user.id, order_pending=True).all()


    history_orders = Bestilling.query.filter_by(bestillings_id=current_user.id, order_pending=False).all()


    return render_template(
        'orders_html.html',
        title=title,
        active_page='orders',
        active_orders = active_orders,
        history_orders = history_orders
    )

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

@ORDERS.route('/orders/update/<int:order_id>', methods=['POST'])
@login_required
def update_order(order_id):
    order = Bestilling.query.get(order_id)
    if order:
        order.mark_order_as_finished()
        flash('Ordre markert som fullført', 'success')
    else:
        flash('Failed to delete order. Order not found.', 'danger')
    return redirect(url_for('orders.orders'))

