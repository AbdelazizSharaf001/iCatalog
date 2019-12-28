#!/usr/bin/env python3
#
# imports	-----------------------
from datetime import datetime

from flask_login import UserMixin

from . import db
from .fn import dump_datetime


# catagories
class Usr(UserMixin, db.Model):
    __tablename__ = 'usr'

    # data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean(), nullable=False, default=False)
    # security
    # - credentials
    email = db.Column(db.String(250), nullable=False, unique=True)
    passwd = db.Column(db.String(250), nullable=False)
    # - alternatives
    public_id = db.Column(db.Integer, nullable=False, unique=True)
    # - (version+)
    public_token = db.Column(db.String(250), nullable=False, unique=True)

    @property
    def serialize(self):
        return {self.public_id: self.name}


# catagories
class Catagory(db.Model):
    __tablename__ = 'catagory'

    # data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    c_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # security
    # - alternatives
    public_id = db.Column(db.Integer, nullable=False, unique=True)

    # ForeignKeys
    usr_id = db.Column(db.Integer, db.ForeignKey('usr.public_id'))

    # relationships
    usr = db.relationship(Usr)

    @property
    def serialize(self):
        return {
            'id': str(self.public_id),
            'name': self.name,
            'last_update': dump_datetime(self.c_date),
            'creator': str(self.usr_id),
        }


# items
class Item(db.Model):
    __tablename__ = 'item'

    # data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(250))
    c_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # price
    price = db.Column(db.Integer, nullable=False, default=0)
    currency = db.Column(db.String(3), nullable=False, default='USD')
    # security
    # - auth
    publish = db.Column(db.Boolean, default=True)
    # - alternatives
    public_id = db.Column(db.Integer, nullable=False, unique=True)

    # ForeignKeys
    usr_id = db.Column(db.Integer, db.ForeignKey('usr.public_id'))
    catagory_id = db.Column(db.Integer, db.ForeignKey('catagory.public_id'))

    # relationships
    usr = db.relationship(Usr)
    catagory = db.relationship(Catagory)

    @property
    def serialize(self):
        return {
            'id': str(self.public_id),
            'name': self.name,
            'description': self.description,
            'last_update': dump_datetime(self.c_date),
            'public': self.publish,
            'catagory_id': str(self.catagory_id),
            'creator': str(self.usr_id),
            'price': [str(self.price), self.currency]
        }
