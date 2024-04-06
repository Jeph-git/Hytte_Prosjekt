from flask import Flask, Blueprint, session, render_template, request
import requests
from flask_login import login_required
 
CABIN_BONDE = Blueprint('cabin_bonde', __name__)

@CABIN_BONDE.route('/cabin_bonde',methods=['POST','GET'])
@login_required
def cabin_bonde():
    if request.method == 'POST':
        message = request.form.get('melding')
        adresse = session['adresse']
        tlfNummer = session['tlfnummer']

        # Construct the data payload
        data = {
            'input': f"{adresse} er brøytet*$*$*{message}*$*$*{tlfNummer}"
        }
        response = requests.post('https://nabohund.no/plowman_cabin/plowman_cabin.php', data=data)
        # Check if the request was successful

        if response.ok:
            tekst =  'Form data sent successfully!'
            return render_template('plwman_cabin_bonde.html', tekst=tekst, RESPONSE=True)
        else:
            tekst = 'Failed to send form data.'
            return render_template('plwman_cabin_bonde.html', tekst=tekst, RESPONSE=True)
        
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
