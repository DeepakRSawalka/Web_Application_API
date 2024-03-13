from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from util.validations import Validation
from util.encrypt import Encryption
from util.db import Users, Assignments, db
import os 
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
import uuid 
import pandas as pd

load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:{os.getenv('DBPORT')}/{os.getenv('DATABASE')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/healthz', methods = ['GET'])
def healthcheck():
    try:
        db.session.execute('SELECT 1')
        res = make_response(jsonify(''), 200)

    except Exception as e:
        res = make_response(jsonify(''), 503)
    
    res.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    return res

@app.route('/healthz', methods = ['POST','PUT','DELETE','PATCH'])
def check():
    res = make_response(jsonify(''), 405)
    return res

def add_users():
    file_path = os.getenv('CSV_PATH', 'users.csv')  # Defaulting if not set  
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Iterate over DataFrame rows
        for index, row in df.iterrows():
            if not all([row['first_name'], row['last_name'], row['email'], row['password']]):
                #logger.error('Enter Valid User data')
                return jsonify(message='Enter Valid User data'), 400

            if Users.query.filter_by(email=row['email']).first():
                #logger.info('User with the same email already exists')
                continue

            hashed_password = Encryption.encrypt(row['password'])
            new_user = Users(
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                password=hashed_password
            )
            db.session.add(new_user)
            

        db.session.commit()
        #logger.info('Users added successfully')
        print("Users added successfully")
        
        return jsonify({"message" : "Users added successfully"}), 201

    except Exception as e:
        #logger.error(f'DB error: {e}')
        return jsonify(message=f'DB error: {e}'), 500
  
@app.route('/v1/assignments', methods = ['POST'])
def create_assignment():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Authentication required"}), 401
    
    email, password = Encryption.decode(auth_header)
    if not Encryption.validate_email(email):
        return jsonify({"message": "Invalid email format"}), 400
    
    user = Encryption.validate_user(email, password)
    if not user:
        return jsonify({"message" : "Invalid credentials"}), 401
    
    data = request.get_json()
    message = Validation.isAssignDataValid(data)
    if message != "":
        # logger.error(message)
        return jsonify({"message" : message}), 400
    
    name = data.get("name")
    points = data.get("points")
    num_of_attempts = data.get("num_of_attempts")
    deadline = data.get("deadline")
    assign = Assignments.query.filter_by(name=name).first()
    if assign:
        # logger.error('User already exist')
        return jsonify({"message":"Assignment already exist"}), 400

    new_assign = Assignments(name=name, points=points, num_of_attempts=num_of_attempts, deadline=deadline, owner_user_id=user.id)
    db.session.add(new_assign)
    try:

        db.session.commit()
        schema = {
            "id": new_assign.id,
            "name": new_assign.name,
            "points": new_assign.points,
            "num_of_attempts": new_assign.num_of_attempts,
            "deadline": new_assign.deadline,
            "assignment_created": new_assign.assignment_created,
            "assignment_updated": new_assign.assignment_updated
        } 
        # logger.info('Create User API ended')
        return schema,201
    except SQLAlchemyError as e:
        db.session.rollback()  # Roll back the session on error
        # logger.error(f"Database error: {str(e)}")
        return jsonify({"message": "Database error, could not create assignment"}), 500


if __name__ == '__main__':
    with app.app_context():
        response, status = add_users()
        print(response.get_json(), status)
    app.run(debug=True)

