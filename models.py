from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case
import datetime

db = SQLAlchemy()

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    seller_name = db.Column(db.String(50))
    buyer_name = db.Column(db.String(50))
    item_id = db.Column(db.Integer)
    price = db.Column(db.Float)
    amount = db.Column(db.Float)


class SellRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_name = db.Column(db.String(50))
    item_id = db.Column(db.Integer)
    price = db.Column(db.Float)
    amount = db.Column(db.Float)

