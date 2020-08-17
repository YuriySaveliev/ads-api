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
    if ad_id not in ADS:
        abort(404, message="Ad {} doesn't exist".format(ad_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

class Ad(Resource):
    def get(self, ad_id):
        abort_if_ad_doesnt_exist(ad_id)
        return ADS[ad_id]

    def delete(self, ad_id):
        abort_if_ad_doesnt_exist(ad_id)
        del ADS[ad_id]
        return '', 204

    def put(self, ad_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        ADS[ad_id] = task
        return task, 201

class AdList(Resource):
    def get(self):
        return ADS

    def post(self):
        args = parser.parse_args()
        ad_id = max(ADS.keys()) + 1
        ADS[ad_id] = {'task': args['task']}
        return ADS[ad_id], 201

api.add_resource(AdList, '/ads')
api.add_resource(Ad, '/ads/<id_id>')


if __name__ == '__main__':
    app.run(debug=True)
