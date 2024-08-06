import requests
import json
from datetime import datetime

from flask import Blueprint
from flask import session
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from flask_login import current_user
from flask_login import login_required


from models import User
from models import Bestilling
from models import Address
from models import User_Customer
from models import Customer

from utils import role_required
from utils import ROLES

from babel.dates import format_datetime
from flask_babel import _


CABIN_BONDE = Blueprint('cabin_bonde', __name__)

@CABIN_BONDE.route('/cabin_bonde', methods=['POST','GET'])
@role_required(ROLES[3])
@login_required
def cabin_bonde():
    if request.method == 'POST':
        message = request.form.get('melding')
        tlfNummer = current_user.phoneNumber
        adresse = session.get('adresse')

        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        formatted_datetime = format_datetime(timestamp_datetime, "d. MMMM yyyy 'kl.' HH:mm", locale='nb_NO')



        default_message = f"Vi har brøytet til din hytte {adresse} i dag {formatted_datetime} vennlig hilsen Plowman"



        address = Address.query.filter_by(address=adresse).first()
        user = User.query.filter_by(id=address.user_id).first()


        user_customer_association = User_Customer.query.filter_by(user_id=user.id).first()


        customer = Customer.query.filter_by(id=user_customer_association.customer_id).first() if user_customer_association else None

        order = Bestilling.query.filter_by(bestillings_id=user.id, order_pending=True).first()

 
        data = {
            'phone': str(tlfNummer),
            'message_from_plowman': str(message),
            'timestamp': str(timestamp),
            'plowman': 'Plowman',
            'default_message': str(default_message),
            'cabin_area': str(customer.name),
        }

        json_data = json.dumps(data)
    

        headers = {'Content-Type': 'application/json'}
        print(f'json_data: {json_data}')
        response = requests.post('https://nabohund.no/plowman_cabin/plowman_cabin.php', data=json_data, headers=headers)
        # return response.text
        
        
        if response.ok: 
            # flash('Brøytet ferdig: Registrert', 'success')
            order.mark_order_as_finished()
            return redirect(url_for('map.map'))
        else:
            # flash('Brøytet ferdig: Feil', 'danger')
            return redirect(url_for('map.map'))

    else:
        title = 'Bestill - Brøyting.net'
        adresse = request.args.get('adresse')
        poststed = request.args.get('poststed')
        postnummer = request.args.get('postnummer')
        session['adresse'] = adresse

        return render_template('plwman_cabin_bonde.html', adresse=adresse, poststed=poststed, postnummer=postnummer, title=title, FORM=True)
        