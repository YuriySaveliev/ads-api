from flask_restful import reqparse, abort, Api, Resource
import sqlite3

class Ad(Resource):
    def get(self, ad_id):
        searcheableAd = {}

        abort_if_ad_doesnt_exist(ad_id)

        for item in ADS:
            if item['id'] == int(ad_id):
                searcheableAd = item

        return searcheableAd     

    def delete(self, ad_id):
        connection = sqlite3.connect('ads.db')
        cursor = connection.cursor()

        parser = reqparse.RequestParser()

        parser.add_argument('id')

        args = parser.parse_args()
        
        cursor.execute("DELETE FROM ads where id=?", (ad_id,))
        connection.commit()

        #abort_if_ad_doesnt_exist(ad_id)

        return '', 204

    def put(self, ad_id):
        args = parser.parse_args()
        ad = {
            "id": args['id'],
            "title": args['title'], 
            "description": args['description'], 
            "price": args['price'],
            "bids": args['bids'] or []
        }

        for item in ADS:
            if item['id'] == int(ad_id):
                item["title"] = args['title'] 
                item["description"] = args['description'] 
                item["price"] = args['price']
                item["bids"] = args['bids'] or []

                return item, 201
