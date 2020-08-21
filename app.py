from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

ADS = [
    {
        'id': 1,
        'title': 'GeForce 1060', 
        'description': 'GDDR5', 
        'price': 150,
        'bids': [
            (100, "2019-01-08 22:17:54"),
            (10, "2019-11-08 22:17:54")
        ]
    },
    {
        'id': 2,
        'title': 'Bike', 
        'description': 'Yamaha', 
        'price': 5000,
        'bids': [
            (4000, "2017-01-08 22:17:54"),
            (4500, "2018-11-08 22:17:54")
        ]
    },
    {
        'id': 3,
        'title': 'Ticket', 
        'description': 'Ticket to the ZOO', 
        'price': 50,
        'bids': [
            (50, "2009-01-08 22:17:54"),
            (10, "2009-11-08 22:17:54")
        ]
    }
]

def abort_if_ad_doesnt_exist(ad_id):
    isAdExist = False

    for item in ADS:
        if item['id'] == int(ad_id):
            isAdExist = True
    
    if (not isAdExist):
        abort(404, message="Ad {} doesn't exist".format(ad_id))

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('description')
parser.add_argument('price')
parser.add_argument('bids')

class Ad(Resource):
    def get(self, ad_id):
        searcheableAd = {}

        abort_if_ad_doesnt_exist(ad_id)

        for item in ADS:
            if item['id'] == int(ad_id):
                searcheableAd = item

        return searcheableAd     

    def delete(self, ad_id):
        newAdsList = []
        global ADS

        abort_if_ad_doesnt_exist(ad_id)

        for item in ADS:
            if item['id'] != int(ad_id):
                newAdsList.append(item)

        ADS = newAdsList[:]
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

class AdList(Resource):
    def get(self):
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

api.add_resource(AdList, '/ads')
api.add_resource(Ad, '/ads/<ad_id>')

if __name__ == '__main__':
    app.run(debug=True)
