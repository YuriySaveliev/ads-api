from app import db


class AdModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(8128))
    price = db.Column(db.Integer)
    bids = db.Column(db.Integer)
    create_date = db.Column(db.String(128))
    image_url = db.Column(db.String(256))
    user_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
