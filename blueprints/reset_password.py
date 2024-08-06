from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import render_template_string
from flask import Blueprint

from flask_login import current_user

from database import db

from models import User

from forms import ResetPasswordRequestForm
from forms import ResetPasswordForm

from flask_mailman import EmailMessage
from flask_mailman import Mail


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
            flash('No user found with that email address.', 'danger')
        return redirect(url_for('login.login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

reset_password_email_html_content = """
<p>Hei,</p>
<p>Du mottar denne e-posten fordi du har bedt om å tilbakestille passordet for kontoen din.</p>
<p>
    For å tilbakestille passordet ditt,
    <a href="{{ reset_password_url }}">klikk her</a>.
</p>
<p>
    Alternativt kan du lime inn følgende lenke i adressefeltet i nettleseren din: <br>
    {{ reset_password_url }}
</p>
<p>Hvis du ikke har bedt om å tilbakestille passordet, vennligst kontakt noen fra utviklingsteamet.</p>
<p>Takk!</p>
"""


@RESET_PASSWORD.route('/reset_password/<token>/<int:user_id>', methods=['GET', 'POST'])
def reset_password(token, user_id):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    user = User.validate_reset_password_token(token, user_id)
    if not user:
        flash('Invalid or expired token.','danger')
        return redirect(url_for('reset_password.reset_password_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
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
