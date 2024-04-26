from flask import Flask, Blueprint, session, redirect, url_for, render_template, flash, request
from flask_login import login_required, logout_user, current_user
from models import User, Bestilling
from utils import role_required, ROLES


ADMIN = Blueprint('admin', __name__)


@ADMIN.route('/admin')
@role_required(ROLES[0])
@login_required
def admin():
    title = 'Admin - Brøyting.net'
    users = User.query.all()
    sorted_users = sorted(users, key=lambda user: user.id) 
    return render_template('admin.html', title=title, active_page='admin', users=sorted_users)

@ADMIN.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@role_required(ROLES[0])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.delete_account()
        flash('User deleted successfully.', 'success')
    else:
        flash('User not found.', 'error')
    return redirect(url_for('admin.admin'))

@ADMIN.route('/admin/delete_order/<int:order_id>', methods=['POST'])
@role_required(ROLES[0])
@login_required
def delete_order(order_id):
    order = Bestilling.query.get(order_id)
    if order:
        order.delete_order(order_id)
        flash('Order deleted successfully.', 'success')
    else:
        flash('Order not found.', 'error')
    return redirect(url_for('admin.admin'))
