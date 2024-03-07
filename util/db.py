from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import psycopg2

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    account_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    account_updated = db.Column(db.DateTime, nullable=False, default=datetime.now())
