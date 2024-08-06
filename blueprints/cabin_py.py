from flask import Blueprint
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for

from blueprints.calender_logic import cal_logic

from flask_login import login_required
from flask_login import current_user

from forms import CalendarForm

from models import Bestilling

from database import db

from utils import role_required
from utils import ROLES




CABIN = Blueprint('cabin', __name__)

@CABIN.route('/cabin',methods=['POST','GET'])
@login_required
@role_required(ROLES[2])
def cabin():
    title='Bestilling - Brøyting.net'
    form = CalendarForm()
    if form.validate_on_submit():
        bruker_id = current_user.id
        formAnkomst = form.ankomst.data
        formAvreise = form.avreise.data
        formMelding = form.melding.data
        if cal_logic(formAnkomst, formAvreise):
            ny_bestilling = Bestilling(ankomst=formAnkomst, avreise=formAvreise, melding=formMelding, bestillings_id=bruker_id, order_pending=True)
            # flash(f'Ankomst {ankomst}, Avreise {avreise}, Melding {melding}', 'success') 
            db.session.add(ny_bestilling)
            db.session.commit()
            flash('Bestilling gjennomført. Se dine bestillinger på "Mine bestillinger"', 'success')
            
            return redirect(url_for('cabin.cabin'))
        else:
            flash('Invalid dato', 'danger')
            return redirect(url_for('cabin.cabin'))
       
    else:
        return render_template('plwman_cabin.html', active_page='cabin', title=title, form=form)