from flask_restful import reqparse, abort, Api, Resource
import sqlite3

class User(Resource):
    def get(self, user_id):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM users where id=?", (user_id,))
        connection.commit()
        row = cursor.fetchone()

        user = {
            'id': row[0],
            'name': row[1], 
            'password': row[2]
        }

        return user

    def delete(self, user_id):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        parser.add_argument('id')
        
        cursor.execute("DELETE FROM users where id=?", (user_id,))
        connection.commit()

        return '', 204

    def put(self, user_id):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        parser = reqparse.RequestParser()

        parser.add_argument('id')
        parser.add_argument('name')
        parser.add_argument('password')

        args = parser.parse_args()
        user = (
            args['id'], 
            args['name'], 
            args['password'],
            user_id
        )
        
        cursor.execute("UPDATE users SET name=?, password=?, where id=?", user)
        connection.commit()

        user = {
            "id": user_id,
            "name": args['name'], 
            "password": args['password']
        }

        return user, 201       
