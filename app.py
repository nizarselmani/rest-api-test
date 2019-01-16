from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    """
    class ItemModel(db.Model):
        __tablename__ = 'items'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.String(80))
        price = db.Column(db.Float(precision=2))

        store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
        store = db.relationship('StoreModel')

    class StoreModel(db.Model):
        __tablename__ = 'stores'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.String(80))

        items = db.relationship('ItemModel', lazy='dynamic')

    class UserModel(db.Model):
        __tablename__ = 'users'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        username = db.Column(db.String(80))
        password = db.Column(db.String(80))
    """
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.__init__(app)
    app.run(debug=True)  # important to mention debug=True
