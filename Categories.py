from flask_restful import reqparse, abort, Api, Resource
import sqlite3
from config import DB_PATH

class Categories(Resource):
    def get(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        categories = []
        
        cursor.execute("SELECT * FROM categories")
        rows = cursor.fetchall()

        for row in rows:
            category = {
                'id': row[0],
                'name': row[1]
            }

            categories.append(dict(category))

        connection.commit()

        return categories
