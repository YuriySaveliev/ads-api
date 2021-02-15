from flask import Flask, redirect, jsonify, request, make_response
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import uuid

from config import DB_PATH
from Ad import Ad
from Ads import AdList
from Categories import Categories

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
api.add_resource(Categories, '/ads/categories')

@app.route('/')
def index():
    return redirect('/ads')

@app.route('/login', methods = ['POST'])
def login_user():
    name = request.json.get('name')
    password = request.json.get('password')

    if name is None or password is None:
        abort(400)
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users where name=?", (name,))
    connection.commit()
    row = cursor.fetchone()

    if row is None:
        return make_response(jsonify({'message': 'Unauthorized access'}), 403)
    
    user = {
        'id': row[0],
        'name': row[1],
        'password': row[2]
    }

    if check_password_hash(user.get('password'), password):
        return jsonify({'status': 'ok', 'user_id': user.get('id'), 'name': user.get('name')})
    else:
        return make_response(jsonify({'message': 'Unauthorized access'}), 403)

@app.route('/register', methods = ['POST'])
def register_user():
    name = request.json.get('name')
    password = request.json.get('password')
    email = request.json.get('email')
    verify_password = request.json.get('verify_password')

    if name is None or password is None or email is None or verify_password is None:
        abort(400)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users where name=?", (name,))
    connection.commit()
    row = cursor.fetchone()

    if row is not None:
        return make_response(jsonify({'message': 'User already exists'}), 400)
    
    password = generate_password_hash(password)
    id = str(uuid.uuid4())
    user = (
        id,
        name,
        password,
        email,
    )

    cursor.execute("INSERT INTO users(id, name, password, email) VALUES(?,?,?,?)", user)
    connection.commit()

    return make_response(jsonify({'name': name}), 400)

if __name__ == '__main__':
    app.run(debug=True)
