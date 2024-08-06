import os
# Flask imports
from flask import Flask
from flask import render_template
from flask import session
from flask_migrate import Migrate
from flask_babel import Babel
from flask_babel import _
from flask_login import LoginManager
from flask_mailman import EmailMessage, Mail

from database import db

# Blueprints imports
from blueprints.login_py import LOGIN, initialize_login_manager
from blueprints.register_py import REGISTER
from blueprints.map import MAP
from blueprints.logout_py import LOGOUT
from blueprints.dashboard_py import DASHBOARD
from blueprints.cabin_py import CABIN
from blueprints.cabin_bonde_py import CABIN_BONDE
from blueprints.profile_py import PROFIL
from blueprints.orders_py import ORDERS
from blueprints.admin import ADMIN
from blueprints.sok_etter_adresse import SOK_ADRESSE
from blueprints.set_password import SET_PASSWORD
from blueprints.calendar import CALENDAR
from blueprints.reset_password import RESET_PASSWORD


app = Flask(__name__, instance_relative_config=True)
login_manager = initialize_login_manager(app)

# Babel to translate to norwegian
babel = Babel(app)
babel.init_app(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'nb_NO'

app.config.update(
    MAIL_SERVER='smtp.mailersend.net',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='MS_pkkTry@trial-z3m5jgryqkd4dpyo.mlsender.net',
    MAIL_PASSWORD='R2eGGBAJjnL4jhHQ',
    MAIL_DEFAULT_SENDER=('Broyting', 'MS_pkkTry@trial-z3m5jgryqkd4dpyo.mlsender.net')
)

mail = Mail(app)


is_heroku = os.environ.get('IS_HEROKU', None)
if is_heroku:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') 
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    app.secret_key = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
else:
    app.config.from_pyfile('config.py') # Secret key and database URI

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/", methods=['POST', 'GET'])
def index(): 
    print(session.get('logged_in'))
    title='Brøyting.net'

    return render_template('index.html',title=title, active_page = 'index')

# Login
app.register_blueprint(LOGIN)

# Logout
app.register_blueprint(LOGOUT)

# Register
app.register_blueprint(REGISTER)

# Map
app.register_blueprint(MAP)

# Cabin for user
app.register_blueprint(CABIN)

# Cabin for bonde
app.register_blueprint(CABIN_BONDE)

# Dashboard
app.register_blueprint(DASHBOARD)

# Profil
app.register_blueprint(PROFIL)

# Orders
app.register_blueprint(ORDERS)

# Admin page
app.register_blueprint(ADMIN)

app.register_blueprint(RESET_PASSWORD)

# Søk adresse
app.register_blueprint(SOK_ADRESSE)

# FOR SETTING THE PASSWORD FOR CREATED ACCOUNTS
app.register_blueprint(SET_PASSWORD)

# PLOWMAN CALENDAR
app.register_blueprint(CALENDAR)

# 404 - Invalid URL
@app.errorhandler(404)
def error_page(e):
    title = '404 - Brøyting.net'
    return render_template('404.html', title=title), 404

# 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    title = '500 - Brøyting.net'
    return render_template('500.html', title=title), 500


if __name__ == '__main__':
    # app.run(debug=True, host= IP) # This one for running on local network
    app.run(debug=True) # This one for checking current-position on map