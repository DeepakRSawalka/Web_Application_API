from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    account_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    account_updated = db.Column(db.DateTime, nullable=False, default=datetime.now())

class Assignments(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    num_of_attempts = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    assignment_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    assignment_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    @validates('points')
    def validate_points(self, key, points):
        if not 1 <= points <= 100:
            raise ValueError("Points must be between 1 and 100")
        return points
    
    @validates('num_of_attempts')
    def validate_attempts(self, key, num_of_attempts):
        if not 1 <= num_of_attempts <= 100:
            raise ValueError("Number of atempts must be between 1 and 100")
        return num_of_attempts
