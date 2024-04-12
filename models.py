from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from datetime import datetime, timezone
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    email = db.Column(db.String(120), unique=True, nullable=True)
    bestillinger = db.relationship('Bestilling', backref='bestiller')

    def __repr__(self):
        return '<User %r>' % self.phoneNumber
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def delete_account(self):
        # Sletter bestillinger
        Bestilling.query.filter_by(bestillings_id=self.id).delete()
        Address.query.filter_by(user_id=self.id).delete()
        db.session.delete(self)
        db.session.commit() 

    def add_email(self, email):
        self.email = email
        db.session.commit()

    def update_email(self, new_email):
        self.email = new_email
        db.session.commit()

class Bestilling(db.Model):
    __tablename__ = 'bestilling'
    id = db.Column(db.Integer, primary_key=True)
    ankomst = db.Column(db.Date, nullable=False)
    avreise = db.Column(db.Date, nullable=False)
    melding = db.Column(db.String(255)) 
    order_pending = db.Column(db.Boolean, default=True)     
    bestillings_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def delete_order(order_id):
        order = Bestilling.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return True
        return False

        
    def mark_order_as_finished(self):
        self.order_pending = False
        db.session.commit()
    
class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    postnummer = db.Column(db.String(10), nullable=False)
    poststed = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Address {self.address}, {self.postnummer}, {self.poststed}>"
    
    def update_address(self, new_address, new_postnummer, new_poststed, new_latitude, new_longitude):
        self.address = new_address
        self.postnummer = new_postnummer
        self.poststed = new_poststed
        self.latitude = new_latitude
        self.longitude = new_longitude
        db.session.commit()