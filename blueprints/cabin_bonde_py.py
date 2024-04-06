from flask import Flask, Blueprint, session, render_template, request, flash, redirect, url_for
from flask_login import current_user
import requests
from database import db
from models import User
from flask_login import login_required
 
CABIN_BONDE = Blueprint('cabin_bonde', __name__)

@CABIN_BONDE.route('/cabin_bonde',methods=['POST','GET'])
@login_required
def cabin_bonde():
    if request.method == 'POST':
        message = request.form.get('melding')
        adresse = session['adresse']
        tlfNummer = current_user.phoneNumber

        # Construct the data payload
        data = {
            'input': f"{adresse} er brøytet*$*$*{message}*$*$*{tlfNummer}"
        }
        response = requests.post('https://nabohund.no/plowman_cabin/plowman_cabin.php', data=data)
        # Check if the request was successful

        if response.ok:
            flash('Brøytet ferdig: Registrert', 'success')
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
        # Process the node information as needed (e.g., save it to a database)

        # return "Node information received: Adresse: {}, Poststed: {}, Postnummer: {}".format(adresse, poststed, postnummer)
        print(session['adresse'])
        return render_template('plwman_cabin_bonde.html', adresse = adresse, poststed = poststed, postnummer=postnummer,title=title, FORM=True)
