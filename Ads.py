from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
from flask import make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import datetime

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'jurassic':
        return 'Welcome1!'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

class AdList(Resource):
    #decorators = [auth.login_required]

    def get(self):
        connection = sqlite3.connect('/home/jurassic987/ads-api/ads.db')
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
        connection = sqlite3.connect('/home/jurassic987/ads-api/ads.db')
        cursor = connection.cursor()

        parser = reqparse.RequestParser()

        parser.add_argument('title')
        parser.add_argument('description')
        parser.add_argument('price')
        parser.add_argument('bids')
        parser.add_argument('image_url')

        args = parser.parse_args()
        ad = (
            args['title'], 
            args['description'], 
            args['price'],
            args['bids'],
            datetime.datetime.now(),
            args['image_url'],
        )

        cursor.execute("INSERT INTO ads(title, description, price, bids, create_date, image_url) VALUES(?,?,?,?,?,?)", ad)
        connection.commit()

        return cursor.lastrowid, 201
