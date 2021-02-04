from flask_restful import reqparse, abort, Api, Resource
from flask_httpauth import HTTPBasicAuth
from flask import make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

auth = HTTPBasicAuth()

users = {
    'regular': generate_password_hash('P@ssword1')
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@auth.get_password
def get_password(username):
    if username == 'jurassic':
        return 'Welcome1!'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

class Ad(Resource):
    #decorators = [auth.login_required]

    def get(self, ad_id):
        connection = sqlite3.connect('ads.db')
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM ads where id=?", (ad_id,))
        connection.commit()
        row = cursor.fetchone()

        #abort_if_ad_doesnt_exist(ad_id)

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
        connection = sqlite3.connect('ads.db')
        cursor = connection.cursor()

        parser.add_argument('id')
        
        cursor.execute("DELETE FROM ads where id=?", (ad_id,))
        connection.commit()

        #abort_if_ad_doesnt_exist(ad_id)

        return '', 204

    def put(self, ad_id):
        connection = sqlite3.connect('ads.db')
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
    
        #abort_if_ad_doesnt_exist(ad_id)
        
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
