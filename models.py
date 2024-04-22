from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from datetime import datetime, timezone
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    role = db.Column(db.String(255), default='cabin_owner') 
    notification_type = db.Column(db.String(255)) 
    email = db.Column(db.String(120), unique=True, nullable=True)
    bestillinger = db.relationship('Bestilling', backref='bestiller')

    def __repr__(self):
        return '<User %r>' % self.phoneNumber
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def delete_account(self):
        # Delete related entries from User_Customer table
        User_Customer.query.filter_by(user_id=self.id).delete()

        # Delete related entries from Governor_Plowman table
        Governor_Plowman.query.filter_by(governor_id=self.id).delete()

        # Delete related entries from Governor_User table
        Governor_User.query.filter_by(governor_id=self.id).delete()

        # Delete associated orders
        Bestilling.query.filter_by(bestillings_id=self.id).delete()

        # Delete associated addresses
        Address.query.filter_by(user_id=self.id).delete()

        # Delete the user itself
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


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(64), nullable=False)
    use_sectors = db.Column(db.Boolean, nullable=False, default=False)
    enable_public_view = db.Column(db.Boolean, default=False, nullable=False)
    use_points = db.Column(db.Boolean)

class Unit_Customer(db.Model):
    __tablename__ = 'unit_customer'
    unit_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))


class Unit_Sector(db.Model):
    __tablename__ = 'unit_sector'
    unit_id = db.Column(db.Integer, db.ForeignKey('unit_customer.unit_id'), primary_key=True)
    sector_id = db.Column(db.Integer)

class User_Customer(db.Model):
    __tablename__ = 'user_customer'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    customer_id = db.Column(db.Integer)


class Governor_Plowman(db.Model):
    __tablename__ = 'governor_plowan'
    governor_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    plowman_id = db.Column(db.Integer)

class Governor_User(db.Model):
    __tablename__ = 'governor_user'
    governor_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user_id = db.Column(db.Integer)