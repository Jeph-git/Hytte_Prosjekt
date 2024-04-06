from flask import Flask, Blueprint, session, redirect, url_for
from flask_login import login_required, logout_user
LOGOUT = Blueprint('logout', __name__)

@LOGOUT.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))