from app import db
from sqlalchemy.ext.associationproxy import association_proxy


class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    book = db.relationship('Booking', backref='bike')




class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bike_id = db.Column(db.Integer, db.ForeignKey('bike.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    start_location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    paid = db.Column(db.Boolean, nullable=False)





class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    bikes = db.relationship('Bike', backref='location')
    book = db.relationship('Booking', backref='location')




class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    firstname = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    book = db.relationship('Booking', backref='account')
    card = db.relationship('Card', backref='account')
    account_type = db.Column(db.Integer, nullable=False)



class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardholder_name = db.Column(db.String(200), nullable=False)
    card_type = db.Column(db.Integer, nullable=False)
    card_number = db.Column(db.Integer, nullable=False)
    card_expiry_date = db.Column(db.DateTime, nullable=False)
    card_address1 = db.Column(db.String(200), nullable=False)
    card_postcode = db.Column(db.String(200), nullable=False)
    card_address2 = db.Column(db.String(200))
    card_city = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
