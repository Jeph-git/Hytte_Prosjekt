from flask import Flask, Blueprint, session, redirect, url_for, render_template, flash
from flask_login import login_required, logout_user, current_user
from models import User, Bestilling
ADMIN = Blueprint('admin', __name__)

@ADMIN.route('/admin')
@login_required
def admin():
    title = 'Admin - Brøyting.net'
    if current_user.id == 33 or current_user.id == 53:  # Replace with appropriate admin ID check
        users = User.query.all()
        sorted_users = sorted(users, key=lambda user: user.id) # So that the newest user is at the bottom
        return render_template('admin.html', title=title, active_page='admin', users=sorted_users)
    else:
        return redirect(url_for('dashboard.dashboard'))
    

@ADMIN.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.id == 33 or current_user.id == 53:  # Replace with appropriate admin ID check
        user = User.query.get(user_id)
        if user:
            user.delete_account()
            flash('User deleted successfully.', 'success')
            # Redirect to the admin page with the user's ID as a parameter
            return redirect(url_for('admin.admin', user_id=user_id, _anchor=f'userModal{user_id}'))
        else:
            flash('User not found.', 'error')
        return redirect(url_for('admin.admin'))
    else:
        return redirect(url_for('dashboard.dashboard'))

@ADMIN.route('/admin/delete_order/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    # Assuming you have appropriate authorization checks here
    
    order = Bestilling.query.get(order_id)
    if order:
        # Delete the order
        order.delete_order(order_id)
        flash('Order deleted successfully.', 'success')
        # Redirect back to the admin page
        return redirect(url_for('admin.admin'))
    else:
        flash('Order not found.', 'error')
        return redirect(url_for('admin.admin'))