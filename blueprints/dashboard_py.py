from flask import Flask, Blueprint, session, redirect, url_for, render_template
from flask_login import login_required

DASHBOARD = Blueprint('dashboard', __name__)

@DASHBOARD.route("/dashboard", methods=['POST', 'GET'])
@login_required
def dashboard():

    title = 'Dashboard - Brøyting.net'
    return render_template('dashboard_html.html', active_page='dashboard', title=title)
    
