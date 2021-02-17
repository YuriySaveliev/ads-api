from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
from flask import make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import datetime
from config import DB_PATH

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(name, password):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users where name=?", (name,))
    connection.commit()
    row = cursor.fetchone()

    user = {
        'id': row[0],
        'name': row[1],
        'password': row[2]
    }

    if check_password_hash(user.get('password'), password):
        return user
    else:
        return make_response(jsonify({'message': 'Unauthorized access'}), 403)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

class AdList(Resource):
    def get(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        ADS = []
        
        cursor.execute("SELECT * FROM ads")
        rows = cursor.fetchall()

        for row in rows:
            ad = {
                'id': row[0],
                'title': row[1], 
                'description': row[2], 
                'price': row[3],
                'bids': row[4],
                'create_date': row[5],
                'image_url': row[6]
            }

            ADS.append(dict(ad))

        connection.commit()

        return ADS

    def post(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        parser = reqparse.RequestParser()

        parser.add_argument('title')
        parser.add_argument('description')
        parser.add_argument('price')
        parser.add_argument('bids')
        parser.add_argument('image_url')

        args = parser.parse_args()

        if not args['title'] or not args['price']:
            return make_response(jsonify({'error': 'Error', 'message': 'One or more fields is required'}), 400)

        if len(args['image_url']) > 256:
            return make_response(jsonify({'error': 'Image error', 'message': 'Image url should contain less than 256 characters'}), 400)
        
        ad = (
            args['title'], 
            args['description'], 
            args['price'],
            args['bids'],
            datetime.datetime.now().isoformat(),
            args['image_url'],
        )

        cursor.execute("INSERT INTO ads(title, description, price, bids, create_date, image_url) VALUES(?,?,?,?,?,?)", ad)
        connection.commit()

        ad = {
                'id': cursor.lastrowid,
                'title': args['title'], 
                'description': args['description'], 
                'price': args['price'],
                'bids': args['bids'],
                'create_date': ad[4],
                'image_url': args['image_url']
            }

        return ad, 201
