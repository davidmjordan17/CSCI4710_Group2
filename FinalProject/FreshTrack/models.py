from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

# User model
# This model represents the user in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))

# GroceryItem model
# This model represents the grocery items in the database
# Each grocery item is associated with a user
class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    expiry_date = db.Column(db.Date)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))  # "Fridge", "Pantry", "Freezer"
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='groceries')