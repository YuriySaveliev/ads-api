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
        connection.close()

        return ADS

    def post(self):
        args = parser.parse_args()
        ad_id = len(ADS) + 1
        ADS.append({
            "id": ad_id,
            "title": args['title'], 
            "description": args['description'], 
            "price": args['price'],
            "bids": args['bids'] or []
        })

        return ADS[ad_id - 1], 201
