from flask_restful import reqparse, abort, Api, Resource
import sqlite3

class AdList(Resource):
    def get(self):
        connection = sqlite3.connect('ads.db')
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
                'bids': row[4]
            }

            ADS.append(dict(ad))

        connection.commit()

        return ADS

    def post(self):
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
            args['bids']
        )

        cursor.execute("INSERT INTO ads(title, description, price, bids) VALUES(?,?,?,?)", ad)
        connection.commit()

        return cursor.lastrowid, 201
