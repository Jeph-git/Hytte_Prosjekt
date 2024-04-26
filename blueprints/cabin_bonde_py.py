from flask import Flask, Blueprint, session, render_template, request, flash, redirect, url_for
from flask_login import current_user
import requests
from database import db
from models import User, Bestilling
from flask_login import login_required
from utils import role_required, ROLES

CABIN_BONDE = Blueprint('cabin_bonde', __name__)

@CABIN_BONDE.route('/cabin_bonde',methods=['POST','GET'])
@role_required(ROLES[3])
@login_required
def cabin_bonde():
    if request.method == 'POST':
        message = request.form.get('melding')
        tlfNummer = current_user.phoneNumber
        adresse = session.get('adresse')
        order = Bestilling.query.filter_by(bestillings_id=current_user.id, order_pending=True).first()

        data = {
            'input': f"{adresse} er brøytet*$*$*{message}*$*$*{tlfNummer}"
        }
        response = requests.post('https://nabohund.no/plowman_cabin/plowman_cabin.php', data=data)


        if response.ok:
            flash('Brøytet ferdig: Registrert', 'success')
            order.mark_order_as_finished()
            return redirect(url_for('map.map'))
        else:
            flash('Brøytet ferdig: Feil', 'danger')
            return redirect(url_for('map.map'))
        
    else:
        title = 'Bestill - Brøyting.net'
        adresse = request.args.get('adresse')
        poststed = request.args.get('poststed')
        postnummer = request.args.get('postnummer')
        session['adresse'] = adresse

        return render_template('plwman_cabin_bonde.html', adresse = adresse, poststed = poststed, postnummer=postnummer,title=title, FORM=True)
