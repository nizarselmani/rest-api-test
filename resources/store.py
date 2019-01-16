from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store is None:
            return {"message":"Store with name {} is not found!"}, 404
        return store.json(), 200

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message":"A store with the name : {} already exists!".format(name)}, 400

        store = StoreModel(name)
        try :
            store.save_to_db()
        except :
            {"message": "An error occurred inserting the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {"message":"Store with name {} is not found!"}, 404

        try:
            store.delete_from_db()
        except:
            {"message": "An error occurred deleting the store."}, 500

        return {"message": "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {"Stores":[store.json() for store in StoreModel.query.all()]}
