from flask import Flask, request, jsonify, make_response
import json 
import requests
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from util.validations import Validation
from util.encrypt import Encryption
from util.db import Users, Assignments, db, Submissions
import boto3
import os 
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
import uuid 
import pandas as pd
import statsd
from app_logging import logger


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:{os.getenv('DBPORT')}/{os.getenv('DATABASE')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

c = statsd.StatsClient('localhost', 8125)

@app.route('/healthz', methods = ['GET'])
def healthcheck():
    c.incr('healthz_counter')
    if request.args:
        logger.error("Query parameters are not allowed", extra={'method': 'GET', 'uri': '/healthz', 'statusCode': 400})
        return jsonify({"message": "Query parameters are not allowed"}), 400
    try:
        if request.data:
            logger.error("Request body should be empty", extra={'method': 'GET', 'uri': '/healthz', 'statusCode': 400})
            return jsonify({"message": "Request body should be empty"}), 400
        
        db.session.execute('SELECT 1')
        res = make_response(jsonify({"message" : "Endpoint is healthy"}), 200)
        logger.info("healthz is working fine", extra={'method': 'GET', 'uri': '/healthz', 'statusCode': 200})

    except Exception as e:
        res = make_response(jsonify({f"message" : {e}}), 503)
        logger.error("healthz is not working server unavailable", extra={'method': 'GET', 'uri': '/healthz', 'statusCode': 503})
    
    res.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    return res

@app.route('/healthz', methods = ['POST','PUT','DELETE','PATCH'])
def check():
    res = make_response(jsonify({"message" : "Method not allowed"}), 405)
    logger.error("Change the method to GET (Method not allowed)", extra={'method': 'GET', 'uri': '/healthz', 'statusCode': 405})
    return res

def add_users():
    file_path = os.getenv('CSV_PATH', 'users.csv')  # Defaulting if not set  
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Iterate over DataFrame rows
        for index, row in df.iterrows():
            if not all([row['first_name'], row['last_name'], row['email'], row['password']]):
                logger.error( "Enter Valid User data", extra={'statusCode': 400})
                return jsonify(message='Enter Valid User data'), 400

            if Users.query.filter_by(email=row['email']).first():
                logger.info("User with the same email already exists")
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
        logger.info("Users added successfully", extra={'statusCode': 201})
        print("Users added successfully")
        
        return jsonify({"message" : "Users added successfully"}), 201

    except Exception as e:
        logger.error(f'Server error: {e}', extra={'statusCode': 500})
        return jsonify(message=f'DB error: {e}'), 500
  
@app.route('/v1/assignments', methods = ['POST'])
def create_assignment():
    c.incr('Create_assignments')
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.error("Authentication required", extra={'method': 'POST', 'uri': '/v1/assignments', 'statusCode': 401})
        return jsonify({"message": "Authentication required"}), 401
    
    email, password = Encryption.decode(auth_header)
    if not Validation.validate_email(email):
        logger.error("Invalid email format", extra={'method': 'POST', 'uri': '/v1/assignments', 'statusCode': 400})
        return jsonify({"message": "Invalid email format"}), 400
    
    user = Validation.validate_user(email, password)
    if not user:
        logger.error("Invalid credentials-Unauthorised", extra={'method': 'POST', 'uri': '/v1/assignments', 'statusCode': 401})
        return jsonify({"message" : "Invalid credentials-Unauthorised"}), 401
    
    data = request.get_json()
    message = Validation.isAssignDataValid(data)
    if message != "":
        logger.error(message, extra={'method': 'POST', 'uri': '/v1/assignments', 'statusCode': 400})
        return jsonify({"message" : message}), 400
    
    name = data.get("name")
    points = data.get("points")
    num_of_attempts = data.get("num_of_attempts")
    deadline = data.get("deadline")
    assign = Assignments.query.filter_by(name=name).first()
    if assign:
        logger.error("Assignment already exist", extra={'method': 'POST', 'uri': '/v1/assignments', 'statusCode': 400})
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
        logger.info(schema, extra={'method': 'POST', 'uri': '/v1/assignments', 'statusCode': 201})
        return schema,201
    except SQLAlchemyError as e:
        db.session.rollback()  # Roll back the session on error
        logger.error(f"Database error, could not create assignment - {e}", extra={'method': 'POST', 'uri': '/v1/assignments', 'statusCode': 500})
        return jsonify({"message": f"Database error, could not create assignment - {e}"}), 500
    
@app.route('/v1/assignments', methods = ['GET'])
def get_assignments():
    c.incr('GET_assignment_list')
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.error("Authentication required", extra={'method': 'GET', 'uri': '/v1/assignments', 'statusCode': 401})
        return jsonify({"message": "Authentication required"}), 401
    
    email, password = Encryption.decode(auth_header)
    if not Validation.validate_email(email):
        logger.error("Invalid email format", extra={'method': 'GET', 'uri': '/v1/assignments', 'statusCode': 400})
        return jsonify({"message": "Invalid email format"}), 400
    
    user = Validation.validate_user(email, password)
    if not user:
        logger.error("Invalid credentials-Unauthorised", extra={'method': 'GET', 'uri': '/v1/assignments', 'statusCode': 401})
        return jsonify({"message" : "Invalid credentials-Unauthorised"}), 401
    
    if request.data:
        logger.error("Request body should be empty", extra={'method': 'GET', 'uri': '/v1/assignments', 'statusCode': 400})
        return jsonify({"message": "Request body should be empty"}), 400
    
    try:
        assignments = Assignments.query.all() 
        if not assignments:
            logger.error("Assignment not found", extra={'method': 'GET', 'uri': '/v1/assignments', 'statusCode': 404})
            return jsonify({"message": "Assignment not found"}), 404
         
        schema = []
        for assignment in assignments:
            result ={
            "id": assignment.id,  
            "name": assignment.name,
            "points": assignment.points,
            "num_of_attempts": assignment.num_of_attempts,
            "deadline": assignment.deadline.isoformat(), 
            "assignment_created": assignment.assignment_created.isoformat(),
            "assignment_updated": assignment.assignment_updated.isoformat()
         }
            schema.append(result)
        logger.info(schema, extra={'method': 'GET', 'uri': '/v1/assignments', 'statusCode': 200})
        return schema,200

    except Exception as e:
        logger.error(f"Server error: {e}", extra={'method': 'GET', 'uri': '/v1/assignments', 'statusCode': 500})
        return jsonify({"message": f"Server error: {e}"}), 500

@app.route('/v1/assignments/<id>', methods = ['GET'])
def get_assignments_details(id):
    c.incr('GET_assignment_details')
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.error("Authentication required", extra={'method': 'GET', 'uri': '/v1/assignments/'+ id, 'statusCode': 401})
        return jsonify({"message": "Authentication required"}), 401
    
    email, password = Encryption.decode(auth_header)
    if not Validation.validate_email(email):
        logger.error("Invalid email format", extra={'method': 'GET', 'uri': '/v1/assignments/'+ id, 'statusCode': 400})
        return jsonify({"message": "Invalid email format"}), 400
    
    user = Validation.validate_user(email, password)
    if not user:
        logger.error("Invalid credentials-Unauthorised", extra={'method': 'GET', 'uri': '/v1/assignments/'+ id, 'statusCode': 401})
        return jsonify({"message" : "Invalid credentials-Unauthorised"}), 401
    
    if request.data:
        logger.error("Request body should be empty", extra={'method': 'GET', 'uri': '/v1/assignments/'+ id, 'statusCode': 400})
        return jsonify({"message": "Request body should be empty"}), 400
    
    try:
        assignments = Assignments.query.filter_by(id=id).first()
        if not assignments:
            logger.error("Assignment not found", extra={'method': 'GET', 'uri': '/v1/assignments/'+ id, 'statusCode': 404})
            return jsonify({"message": "Assignment not found"}), 404
         
        schema = {
        "id": assignments.id,  
        "name": assignments.name,
        "points": assignments.points,
        "num_of_attempts": assignments.num_of_attempts,
        "deadline": assignments.deadline.isoformat(), 
        "assignment_created": assignments.assignment_created.isoformat(),
        "assignment_updated": assignments.assignment_updated.isoformat()
         }
        
        logger.info(schema, extra={'method': 'GET', 'uri': '/v1/assignments/'+ id, 'statusCode': 200})  
        return schema,200

    except Exception as e:
        logger.error(f"Server error: {e}", extra={'method': 'GET', 'uri': '/v1/assignments/'+ id, 'statusCode': 500})
        return jsonify({"message": f"Server error: {e}"}), 500

@app.route('/v1/assignments/<id>', methods = ['PUT'])
def update_assignments(id):
    c.incr('Update_assignments')
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.error("Authentication required", extra={'method': 'PUT', 'uri': '/v1/assignments/'+ id, 'statusCode': 401})
        return jsonify({"message": "Authentication required"}), 401
    
    email, password = Encryption.decode(auth_header)
    if not Validation.validate_email(email):
        logger.error("Invalid email format", extra={'method': 'PUT', 'uri': '/v1/assignments/'+ id, 'statusCode': 400})
        return jsonify({"message": "Invalid email format"}), 400
    
    user = Validation.validate_user(email, password)
    if not user:
        logger.error("Invalid credentials-Unauthorised", extra={'method': 'PUT', 'uri': '/v1/assignments/'+ id, 'statusCode': 401})
        return jsonify({"message" : "Invalid credentials-Unauthorised"}), 401
    
    try:
        assignments = Assignments.query.filter_by(id=id).first()

        if assignments.owner_user_id != user.id:
            logger.error("User does not have necessary permissions to Update-Forbidden", extra={'method': 'PUT', 'uri': '/v1/assignments/'+ id, 'statusCode': 403})
            return jsonify({"message": "User does not have necessary permissions to Update-Forbidden"}), 403

        if not assignments:
            logger.error("Assignment not found", extra={'method': 'PUT', 'uri': '/v1/assignments/'+ id, 'statusCode': 404})
            return jsonify({"message": "Assignment not found"}), 404
        
        data = request.get_json()
        message = Validation.isAssignDataValid(data)
        if message != "":
            logger.error(message, extra={'method': 'PUT', 'uri': '/v1/assignments/'+ id, 'statusCode': 400})
            return jsonify({"message" : message}), 400
    
        assignments.name = data.get("name")
        assignments.points = data.get("points")
        assignments.num_of_attempts = data.get("num_of_attempts")
        assignments.deadline = data.get("deadline")
         
        db.session.commit()

        logger.info("Assignment updated Successfully!!", extra={'method': 'PUT', 'uri': '/v1/assignments/'+ id, 'statusCode': 204}) 
        return {},204

    except Exception as e:
        logger.error(f"Server error: {e}", extra={'method': 'PUT', 'uri': '/v1/assignments/'+ id, 'statusCode': 500})
        return jsonify({"message": f"Server error: {e}"}), 500
    

@app.route('/v1/assignments/<id>', methods = ['DELETE'])
def delete_assignments(id):
    c.incr('Delete_assignments')
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.error("Authentication required", extra={'method': 'DELETE', 'uri': '/v1/assignments/'+ id, 'statusCode': 401})
        return jsonify({"message": "Authentication required"}), 401
    
    email, password = Encryption.decode(auth_header)
    if not Validation.validate_email(email):
        logger.error("Invalid email format", extra={'method': 'DELETE', 'uri': '/v1/assignments/'+ id, 'statusCode': 400})
        return jsonify({"message": "Invalid email format"}), 400
    
    user = Validation.validate_user(email, password)
    if not user:
        logger.error("Invalid credentials-Unauthorised", extra={'method': 'DELETE', 'uri': '/v1/assignments/'+ id, 'statusCode': 401})
        return jsonify({"message" : "Invalid credentials-Unauthorised"}), 401
    
    try:
        assignments = Assignments.query.filter_by(id=id).first()

        if assignments.owner_user_id != user.id:
            logger.error("User does not have necessary permissions to Delete-Forbidden", extra={'method': 'DELETE', 'uri': '/v1/assignments/'+ id, 'statusCode': 403})
            return jsonify({"message": "User does not have necessary permissions to Delete-Forbidden"}), 403

        if request.data:
            logger.error("Request body should be empty", extra={'method': 'DELETE', 'uri': '/v1/assignments/'+ id, 'statusCode': 400})
            return jsonify({"message": "Request body should be empty"}), 400
    
        if not assignments:
            logger.error("Assignment not found", extra={'method': 'DELETE', 'uri': '/v1/assignments/'+ id, 'statusCode': 404})
            return jsonify({"message": "Assignment not found"}), 404

        db.session.delete(assignments)
        db.session.commit()
        
        logger.info("Assignment Deleted Successfully!!", extra={'method': 'DELETE', 'uri': '/v1/assignments/'+ id, 'statusCode': 204})
        return {},204

    except Exception as e:
        logger.error(f"Server error: {e}", extra={'method': 'DELETE', 'uri': '/v1/assignments/'+ id, 'statusCode': 500})
        return jsonify({"message": f"Server error: {e}"}), 500
    
@app.route('/v1/assignments/<id>', methods = ['PATCH'])
def update(id):
    c.incr('Patch_assignments')
    logger.error("Method Not allowed", extra={'method': 'PATCH', 'uri': '/v1/assignments/'+ id, 'statusCode': 405})
    return {},405



@app.route('/v1/assignments/<id>/submission', methods = ['POST'])
def create_submission(id):
    c.incr('Create_submissions')
    # Initialize Boto3 SNS client
    sns_client = boto3.client('sns', region_name=os.getenv('AWS_REGION'))
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.error("Authorization required", extra={'method': 'POST', 'uri': '/v1/assignments/'+ id +'/submission', 'statusCode': 401})
        return jsonify({"message": "Authorization required"}), 401
    
    email,password = Encryption.decode(auth_header)
    if not Validation.validate_email(email):
        logger.error("Invalid email format", extra={'method': 'POST', 'uri': '/v1/assignments/'+ id +'/submission', 'statusCode': 400})
        return jsonify({"message": "Invalid email format"}), 400
    
    data = request.get_json()
    submission_url= data.get("submission_url")
    message = Validation.isSubDataValid(data)
    if message != "":

        failure_message = {
            "submission_url": submission_url,
            "email": email,
            "status": 'invalid_url'
        }

        sns_client.publish(
            TopicArn=os.getenv('SNS_TOPIC_ARN'),
            Message=json.dumps({'default': json.dumps(failure_message)}),
            MessageStructure='json'
        )

        logger.error(message, extra={'method': 'POST', 'uri': '/v1/assignments/'+ id +'/submission', 'statusCode': 400})
        return jsonify({"message" : message}), 400
    
    
    assign = Assignments.query.filter_by(id=id).first()
    user = Users.query.filter_by(email=email).first()
    if not assign:
        logger.error("Assignment Not found", extra={'method': 'POST', 'uri': '/v1/assignments/'+ id +'/submission', 'statusCode': 404})
        return jsonify({"message":"Assignment Not found"}), 404
    
    # Check if the deadline has passed
    if datetime.now(timezone.utc) > assign.deadline:
        logger.error("Deadline has passed", extra={'method': 'POST', 'uri': '/v1/assignments/'+ id +'/submission', 'statusCode': 400})
        return jsonify({"message": "Deadline has passed"}), 400
    
    # Check the number of attempts
    submission_count = Submissions.query.filter_by(assignment_id=assign.id).count()
    if submission_count >= assign.num_of_attempts:
        logger.error("Maximum number of attempts exceeded", extra={'method': 'POST', 'uri': '/v1/assignments/'+ id +'/submission', 'statusCode': 400})
        return jsonify({"message": "Maximum number of attempts exceeded"}), 400

    new_sub = Submissions(submission_url=submission_url, assignment_id=assign.id)
    db.session.add(new_sub)
    try:    

        response = requests.head(submission_url)
        # Sending SNS message
        message = {
            "submission_url": submission_url,
            "email": email,
            "user_name": user.first_name,
            "user_id": user.id,
            "assignment_id": id,
            "status": "valid"
        }
        sns_client.publish(
            TopicArn=os.getenv('SNS_TOPIC_ARN'),
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )

        db.session.commit()
        schema = {
            "id": new_sub.id,
            "assignment_id": assign.id,
            "submission_url": new_sub.submission_url,
            "submission_date": new_sub.submission_date,
            "submission_updated": new_sub.submission_updated
        } 
        logger.info(schema, extra={'method': 'POST', 'uri': '/v1/assignments/'+ id +'/submission', 'statusCode': 201})
        return schema,201
    except Exception as e:

        if response.status_code != 200:
            failure_message = {
            "submission_url": submission_url,  
            "email": email,
            "status": "no_file"
            }
        
            sns_client.publish(
                Message=json.dumps(failure_message),
                TopicArn=os.getenv('SNS_TOPIC_ARN')
            )
        
            logger.error(f"HTTP error on submission: {e}", extra={'method': 'POST', 'uri': '/v1/assignments/'+ id +'/submission', 'statusCode': 404})
            return jsonify({"message": "Submission URL could not be reached"}), 404

        else:

            db.session.rollback()  # Roll back the session on error
            logger.error(f"Database error, could not submit assignment - {e}", extra={'method': 'POST', 'uri':'/v1/assignments/'+ id +'/submission', 'statusCode': 500})
            return jsonify({"message": f"Database error, could not submit assignment - {e}"}), 500


if __name__ == '__main__':
    with app.app_context():
        response, status = add_users()
        print(response.get_json(), status)
    app.run(host="0.0.0.0",debug=True)

