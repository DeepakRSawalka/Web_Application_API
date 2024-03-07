from flask import Flask, request, jsonify,make_response
from dotenv import load_dotenv
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from util.validations import Validation
from util.encrypt import Encryption
from util.db import Users, db
import os 
import psycopg2
import uuid 
import pandas as pd

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
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
                print('User already exists')
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
        
        return jsonify(message = 'Users added successfully'), 201

    except Exception as e:
        #logger.error(f'DB error: {e}')
        return jsonify(message=f'DB error: {e}'), 500
'''  
@app.route('/v1/assignments', methods = ['POST'])
def create_assignment():
    data = request.get_json()
    message = Validation.isUserDataValid(data)
    if message != "":
        # logger.error(message)
        return {"message" : message},400
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    user = Users.query.filter_by(email=email).first()
    if user:
        # logger.error('User already exist')
        return {"message":"User already exist"},400

    password = Encryption.encrypt(password)
    new_user = Users(first_name=first_name, last_name=last_name, email=email, password=password)
    db.session.add(new_user)
    user = Users.query.filter_by(email=email).first()
    db.session.commit()
    schema = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "account_created": user.account_created,
        "account_updated": user.account_updated
    } 
    # logger.info('Create User API ended')
    return schema,201
'''

if __name__ == '__main__':
    with app.app_context():
        response, status = add_users()
        print(response.get_json(), status)
    app.run(debug=True)

