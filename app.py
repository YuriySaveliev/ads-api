import sqlite3
import uuid
from datetime import datetime

from flask import Flask, redirect, jsonify, request, make_response, url_for
from flask_restful import abort, Api
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import DB_PATH

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ads.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
api = Api(app)

class AdModel(db.Model):
    __tablename__ = 'ads'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(8128))
    price = db.Column(db.Integer)
    bids = db.Column(db.Integer)
    create_date = db.Column(db.String(128))
    image_url = db.Column(db.String(256))
    user_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)

class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))

'''def abort_if_ad_doesnt_exist(ad_id):
    isAdExist = False

    for item in ADS:
        if item['id'] == int(ad_id):
            isAdExist = True
    
    if (not isAdExist):
        abort(404, message="Ad {} doesn't exist".format(ad_id))'''

@app.route('/')
def index():
    return redirect('/ads')

@app.route('/ads', methods=['GET'])
def get_ads():
    ads = AdModel.query.all()
    res = []

    for row in ads:
        ad = {
            'id': row.id,
            'title': row.title,
            'description': row.description,
            'price': row.price,
            'bids': row.bids,
            'create_date': row.create_date,
            'image_url': row.image_url,
            'user_id': row.user_id
        }

        res.append(ad)

    return make_response(jsonify(res))

@app.route('/ads', methods=['POST'])
def add_ad():
    data = request.get_json() or {}

    if not data['title'] or not data['price']:
        return make_response(jsonify({'error': 'Error', 'message': 'One or more fields is required'}), 400)

    if len(data['image_url']) > 256:
        return make_response(jsonify({'error': 'Image error', 'message': 'Image url should contain less than 256 characters'}), 400)

    data['create_date'] = datetime.now().isoformat()
    data['user_id'] = None
    data['category_id'] = None

    ad = AdModel(title=data['title'], description=data['description'], price=data['price'], bids=data['bids'], create_date=data['create_date'], image_url=data['image_url'], user_id=data['user_id'], category_id=data['category_id'])
    db.session.add(ad)
    db.session.commit()
    created_ad = {
        'id': ad.id,
        'title': ad.title,
        'description': ad.description,
        'price': ad.price,
        'bids': ad.bids,
        'create_date': ad.create_date,
        'image_url': ad.image_url,
        'user_id': ad.user_id,
        'category_id': ad.category_id
    }
    response = jsonify(created_ad)
    response.status_code = 201
    #response.headers['Location'] = url_for('get_ad', id=ad.id)

    return response

@app.route('/ads/<int:id>', methods=['GET'])
def get_ad(id):
    ad = AdModel.query.get_or_404(id)
    result = {
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'price': ad.price,
            'bids': ad.bids,
            'create_date': ad.create_date,
            'image_url': ad.image_url,
            'user_id': ad.user_id
        }

    return jsonify(result)

@app.route('/ads/<int:id>', methods=['DELETE'])
def delete_ad(id):
    ad = AdModel.query.get(id)
    db.session.delete(ad)
    db.session.commit()

    response = jsonify()
    response.status_code = 201
    return response

@app.route('/ads/<int:id>', methods=['PUT'])
def update_ad(id):
    ad = AdModel.query.get_or_404(id)
    data = request.get_json() or {}

    if not data['title'] or not data['price']:
        return make_response(jsonify({'error': 'Error', 'message': 'One or more fields is required'}), 400)

    if len(data['image_url']) > 256:
        return make_response(
            jsonify({'error': 'Image error', 'message': 'Image url should contain less than 256 characters'}), 400)

    '''if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')'''

    ad.title = data['title']
    ad.description = data['description']
    ad.price = data['price']
    ad.bids = data['bids']
    ad.image_url = data['image_url']
    ad.user_id = data['user_id']
    ad.category_id = data['category_id']

    updated_ad = {
        'id': ad.id,
        'title': ad.title,
        'description': ad.description,
        'price': ad.price,
        'bids': ad.bids,
        'create_date': ad.create_date,
        'image_url': ad.image_url,
        'user_id': ad.user_id,
        'category_id': ad.category_id
    }
    db.session.commit()
    return jsonify(updated_ad)

@app.route('/ads/categories', methods=['GET'])
def get_categories():
    categories = CategoryModel.query.all()
    res = []

    for row in categories:
        category = {
            'id': row.id,
            'name': row.name
        }

        res.append(category)

    return make_response(jsonify(res))

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
