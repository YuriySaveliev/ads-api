from flask_restful import reqparse, abort, Api, Resource
import sqlite3

class Ad(Resource):
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
            'bids': row[4]
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

        args = parser.parse_args()
        ad = (
            args['title'], 
            args['description'], 
            args['price'],
            args['bids'],
            ad_id
        )
    
        #abort_if_ad_doesnt_exist(ad_id)
        
        cursor.execute("UPDATE ads SET title=?, description=?, price=?, bids=? where id=?", ad)
        connection.commit()

        ad = {
            "id": ad_id,
            "title": args['title'], 
            "description": args['description'], 
            "price": args['price'],
            "bids": args['bids']
        }

        return ad, 201       
