from flask import render_template, redirect, url_for, flash, render_template_string, Blueprint
from flask_login import current_user
from database import db
from models import User
from forms import ResetPasswordRequestForm, ResetPasswordForm
from flask_mailman import EmailMessage, Mail

RESET_PASSWORD = Blueprint('reset_password', __name__)


mail = Mail()
@RESET_PASSWORD.record_once
def init_mail(state):
    app = state.app
    mail.init_app(app)
@RESET_PASSWORD.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_password_email(user)
            flash('An email has been sent with instructions to reset your password.', 'success')
        else:
            flash('No user found with that email address.')
        return redirect(url_for('login.login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

reset_password_email_html_content = """
<p>Hello,</p>
<p>You are receiving this email because you requested a password reset for your account.</p>
<p>
    To reset your password,
    <a href="{{ reset_password_url }}">click here</a>.
</p>
<p>
    Alternatively, you can paste the following link in your browser's address bar: <br>
    {{ reset_password_url }}
</p>
<p>If you have not requested a password reset, please contact someone from the development team.</p>
<p>Thank you!</p>
"""

@RESET_PASSWORD.route('/reset_password/<token>/<int:user_id>', methods=['GET', 'POST'])
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    user = User.validate_reset_password_token(token, user_id)
    if not user:
        flash('Invalid or expired token.')
        return redirect(url_for('reset_password.reset_password_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)

def send_reset_password_email(user):
    reset_password_url = url_for(
        'reset_password.reset_password',
        token=user.generate_reset_password_token(),
        user_id=user.id,
        _external=True,
    )

    email_body = render_template_string(
        reset_password_email_html_content, reset_password_url=reset_password_url
    )

    message = EmailMessage(
        subject="Reset your password",
        body=email_body,
        to=[user.email],
    )
    message.content_subtype = "html"

    message.send()
