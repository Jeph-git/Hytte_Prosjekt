from flask import Flask, Blueprint, session, redirect, url_for, render_template, flash, request
from models import User, Bestilling, Customer, User_Customer, Governor_User, Governor_Plowman
from flask_login import current_user, login_required
from database import db
from utils import role_required, ROLES
from forms import SelectCustomer
# from roles import ROLES

ORDERS = Blueprint('orders', __name__)


@ORDERS.route('/orders', methods=['GET', 'POST'])
@role_required(ROLES[1], ROLES[2], ROLES[3])
@login_required
def orders():

    title = 'Bestillinger - Brøyting.net'
    if current_user.role == ROLES[2] or ROLES[0]: # cabin_owner
        # Får alle bestillinger som samsvarer med ID'en til den påloggede
        active_orders = Bestilling.query.filter_by(bestillings_id=current_user.id, order_pending=True).all()

        history_orders = Bestilling.query.filter_by(bestillings_id=current_user.id, order_pending=False).all()

        return render_template(
            'orders_html.html',
            title=title,
            active_page='orders',
            active_orders = active_orders,
            history_orders = history_orders,
        )
    elif current_user.role == ROLES[1]: # Governor
        #  Finner alle ID'ene i governor_user som er linket til den påloggede governor
        governor_user_ids = Governor_User.query.filter_by(governor_id=current_user.id).all()

        user_ids = [governor_user.user_id for governor_user in governor_user_ids]

        active_orders = Bestilling.query.filter(Bestilling.bestillings_id.in_(user_ids), Bestilling.order_pending == True).all()

        history_orders = Bestilling.query.filter(Bestilling.bestillings_id.in_(user_ids), Bestilling.order_pending == False).all()
        return render_template(
            'orders_html.html',
            title=title,
            active_page='orders',
            active_orders = active_orders,
            history_orders = history_orders,
        )
    
    elif current_user.role == ROLES[3]:  # Plowman
        form = SelectCustomer()

        
        # Finn alle kunder som er linket til Plowman
        customers = Customer.query.join(User_Customer).filter(User_Customer.user_id == current_user.id).all()

        
        # Fyll valgene for SelectField med kundenavn og IDer
        form.customer.choices = [(customer.id, customer.name) for customer in customers]

        if form.validate_on_submit():
            selected_customer_id = form.customer.data
        else:

            # Vis skjemaet for å velge en kunde
            return render_template('orders_html_plowman.html', title=title, active_page='orders', form=form)

        if selected_customer_id:
            user_ids = [uc.user_id for uc in User_Customer.query.filter_by(customer_id=selected_customer_id).all()]
            active_orders = Bestilling.query.filter(Bestilling.bestillings_id.in_(user_ids), Bestilling.order_pending == True).all()
            history_orders = Bestilling.query.filter(Bestilling.bestillings_id.in_(user_ids), Bestilling.order_pending == False).all()
            
            return render_template('orders_html_plowman.html', title=title, active_page='orders', active_orders=active_orders, history_orders=history_orders, form=form)
        else:

            # Håndter tilfelle der ingen kunde er valgt
            return "No customer selected"





@ORDERS.route('/orders/delete/<int:order_id>', methods=['POST'])
@role_required(ROLES[1], ROLES[2], ROLES[3])
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
@role_required(ROLES[1], ROLES[2], ROLES[3])
@login_required
def update_order(order_id):
    order = Bestilling.query.get(order_id)
    if order:
        order.mark_order_as_finished()
        flash('Ordre markert som fullført', 'success')
    else:
        flash('Failed to delete order. Order not found.', 'danger')
    return redirect(url_for('orders.orders'))

