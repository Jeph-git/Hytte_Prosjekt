from flask import Flask, url_for, render_template, request, session, redirect, Blueprint
from database import db
from datetime import datetime
import json
from flask_login import login_required

MAP = Blueprint('map', __name__)

@MAP.route('/map', methods=['POST', 'GET'])
@login_required
def map():
    title='Kart - Brøyting.net'
    session.pop('adresse', None)
    with open('map/config_kvam.json', encoding='utf-8') as config_file:
        config_data = json.load(config_file)

    with open('map/kvam_data.json', encoding='utf-8') as gjetargut_file:
        gjetargut_data = json.load(gjetargut_file)
    return render_template('map.html', config=config_data, markers=gjetargut_data[0]['adresser'], active_page='map',title=title)
    