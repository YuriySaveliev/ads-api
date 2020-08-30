from flask import Flask, redirect
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import sqlite3

from Ad import Ad
from Ads import AdList

app = Flask(__name__)
CORS(app)
api = Api(app)

def abort_if_ad_doesnt_exist(ad_id):
    isAdExist = False

    for item in ADS:
        if item['id'] == int(ad_id):
            isAdExist = True
    
    if (not isAdExist):
        abort(404, message="Ad {} doesn't exist".format(ad_id))

api.add_resource(AdList, '/ads')
api.add_resource(Ad, '/ads/<ad_id>')

@app.route('/')
def index():
    return redirect('/ads')

if __name__ == '__main__':
    app.run(debug=True)
