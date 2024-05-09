from flask import Flask, Blueprint, session, redirect, url_for, render_template, flash, request
from models import User, Bestilling, Customer, User_Customer, Governor_User, Governor_Plowman
from flask_login import current_user, login_required
from database import db
from utils import role_required, ROLES
from forms import SelectCustomer

ORDERS = Blueprint('orders', __name__)


@ORDERS.route('/orders', methods=['GET', 'POST'])
@role_required(ROLES[1], ROLES[2], ROLES[3])
@login_required
def orders():
    title = 'Bestillinger - Brøyting.net'
    if current_user.role == 'cabin_owner': # cabin_owner
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
    if current_user.role == 'governor': # Governor
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
    
    if current_user.role == 'plowman':  # Plowman
        title = 'Bestillinger'
        form = SelectCustomer()


        customer_count = len(User_Customer.query.filter_by(user_id=current_user.id).all())
        
        selected_customer_id = None
        if customer_count > 0:
            selected_customer_id = User_Customer.query.filter_by(user_id=current_user.id).first().customer_id

        customers = Customer.query.join(User_Customer).filter(User_Customer.user_id == current_user.id).all()
        form.customer.choices = [(customer.id, customer.name) for customer in customers]

        if form.validate_on_submit():
            selected_customer_id = form.customer.data

        if selected_customer_id:
            user_ids = [uc.user_id for uc in User_Customer.query.filter_by(customer_id=selected_customer_id).all()]
            active_orders = Bestilling.query.filter(Bestilling.bestillings_id.in_(user_ids), Bestilling.order_pending == True).all()
            history_orders = Bestilling.query.filter(Bestilling.bestillings_id.in_(user_ids), Bestilling.order_pending == False).all()

            return render_template('orders_html_plowman.html', title=title, active_page='orders', active_orders=active_orders, history_orders=history_orders, form=form)


        return render_template('orders_html_plowman.html', title=title, active_page='orders', form=form)

@ORDERS.route('/order_plowman', methods=['GET', 'POST'])
@role_required(ROLES[3])
@login_required
def display_orders():
    title = 'Bestillinger'
    form = SelectCustomer()


    customer_count = len(User_Customer.query.filter_by(user_id=current_user.id).all())
    
    selected_customer_id = None
    if customer_count > 0:
        selected_customer_id = User_Customer.query.filter_by(user_id=current_user.id).first().customer_id

    customers = Customer.query.join(User_Customer).filter(User_Customer.user_id == current_user.id).all()
    form.customer.choices = [(customer.id, customer.name) for customer in customers]

    if form.validate_on_submit():
        selected_customer_id = form.customer.data

    if selected_customer_id:
        user_ids = [uc.user_id for uc in User_Customer.query.filter_by(customer_id=selected_customer_id).all()]
        active_orders = Bestilling.query.filter(Bestilling.bestillings_id.in_(user_ids), Bestilling.order_pending == True).all()
        history_orders = Bestilling.query.filter(Bestilling.bestillings_id.in_(user_ids), Bestilling.order_pending == False).all()

        return render_template('orders_html_plowman.html', title=title, active_page='orders', active_orders=active_orders, history_orders=history_orders, form=form)


    return render_template('orders_html_plowman.html', title=title, active_page='orders', form=form)



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

