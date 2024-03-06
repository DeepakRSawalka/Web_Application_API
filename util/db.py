from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import psycopg2

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
