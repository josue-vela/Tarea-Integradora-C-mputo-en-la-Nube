from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Arrival(db.Model):
    __tablename__ = 'arrival'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #parking_name = db.Column(db.Integer, db.ForeignKey('parking.name'))


class Parking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    cp = db.Column(db.String(10), nullable=False)
    tel = db.Column(db.String(10), nullable=False)
    cap = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), unique=True, nullable=False)
    date_add = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Note')
