from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import flash

from flask_login import logout_user

from models import db
from models import User

from utils import verify_token

from forms import SetPasswordForm


SET_PASSWORD = Blueprint('user', __name__)

@SET_PASSWORD.route('/set_password/<token>', methods=['GET', 'POST'])
def set_password(token):
    logout_user()
    form = SetPasswordForm()
    if form.validate_on_submit():
        user_id = verify_token(token)
        if user_id:
            user = User.query.get(user_id)
            if user:
                phoneNumber = user.phoneNumber
                # Check if pw match
                if form.password.data == form.confirmPassword.data:
                    user.set_password(form.password.data)
                    db.session.commit()
                    return redirect(url_for('login.login', phoneNumber=phoneNumber))
                else:
                    flash('Passordene matcher ikke', 'danger')
                    return render_template('set_password.html', token=token, form=form)
            else:
                flash('User not found', 'danger')
                return redirect(url_for('login.login'))
        else:
            flash('Invalid token', 'danger')
            return redirect(url_for('login.login'))
    else:
        return render_template('set_password.html', token=token, form=form)
