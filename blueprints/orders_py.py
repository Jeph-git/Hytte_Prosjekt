from flask import Flask, Blueprint, session, redirect, url_for, render_template, flash, request
from models import User, Bestilling
from flask_login import current_user, login_required
from database import db


ORDERS = Blueprint('orders', __name__)


@ORDERS.route('/orders')
@login_required
def orders():
    title = 'Bestillinger - Brøyting.net'
    
    # Query the database to retrieve the active orders for the current user
    active_orders = Bestilling.query.filter_by(bestillings_id=current_user.id, order_pending=True).all()

    # Query the database to retrieve the historical orders for the current user
    history_orders = Bestilling.query.filter_by(bestillings_id=current_user.id, order_pending=False).all()

    # Pagination for active orders
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(active_orders) + per_page - 1) // per_page
    active_orders_per_page = active_orders[start:end]
    history_orders_per_page = history_orders[start:end]

    # Render the template with the orders data
    return render_template(
        'orders_html.html',
        title=title,
        active_page='orders',
        total_pages=total_pages,
        page=page,
        per_page=per_page,
        active_orders_per_page=active_orders_per_page,
        history_orders_per_page=history_orders_per_page
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

