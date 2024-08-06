from flask import Blueprint
from flask import redirect
from flask import url_for

from flask_login import login_required
from flask_login import logout_user


LOGOUT = Blueprint('logout', __name__)

@LOGOUT.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))