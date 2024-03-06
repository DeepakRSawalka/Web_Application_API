from flask import Flask, request, jsonify,make_response
from dotenv import load_dotenv
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from util.db import init_db, db
import os 
import psycopg2

load_dotenv()

app = Flask(__name__)

username = os.getenv('DBUSER')
pwd = os.getenv('DBPASS')
host = os.getenv('DBHOST')
dbname = os.getenv('DATABASE')
dbport = os.getenv('DBPORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{username}:{pwd}@{host}:{dbport}/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


@app.route('/healthz', methods = ['GET'])
def healthcheck():
    try:
        db.session.execute('SELECT 1')
        res = make_response(jsonify({}), 200)

    except Exception as e:
        res = make_response(jsonify({}), 503)
    
    res.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    return res

@app.route('/healthz', methods = ['POST','PUT','DELETE','PATCH'])
def check():
    res = make_response(jsonify({}), 405)
    return res

if __name__ == '__main__':
    app.run(debug=True)

