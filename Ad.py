from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
from flask import make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

auth = HTTPBasicAuth()

class Ad(Resource):
    def get(self, ad_id):
        connection = sqlite3.connect('/home/jurassic987/ads-api/ads.db')
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM ads where id=?", (ad_id,))
        connection.commit()
        row = cursor.fetchone()

        ad = {
            'id': row[0],
            'title': row[1], 
            'description': row[2], 
            'price': row[3],
            'bids': row[4],
            'create_date': row[5],
            'image_url': row[6]
        }

        return ad

    def delete(self, ad_id):
        connection = sqlite3.connect('/home/jurassic987/ads-api/ads.db')
        cursor = connection.cursor()

        parser = reqparse.RequestParser()
        parser.add_argument('id')
        
        cursor.execute("DELETE FROM ads where id=?", (ad_id,))
        connection.commit()

        return '', 204

    def put(self, ad_id):
        connection = sqlite3.connect('/home/jurassic987/ads-api/ads.db')
        cursor = connection.cursor()

        parser = reqparse.RequestParser()

        parser.add_argument('id')
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
            args['image_url'],
            ad_id
        )
        
        cursor.execute("UPDATE ads SET title=?, description=?, price=?, bids=?, image_url=? where id=?", ad)
        connection.commit()

        ad = {
            "id": ad_id,
            "title": args['title'], 
            "description": args['description'], 
            "price": args['price'],
            "bids": args['bids'],
            "create_date": args['create_date'],
            "image_url": args['image_url'],
        }

        return ad, 201       
