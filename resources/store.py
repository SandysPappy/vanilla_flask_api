from flask_restful import Resource, reqparse
from models.store_model import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('description',
        type=str,
        required=False,
        help="Please insert an optional description of this current store"
    )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'That Store already exists'}, 400

        data = self.parser.parse_args()
        store = store = StoreModel(name, data['description'])

        try:
            store.save_to_db()
        except:
            return {'message': 'Error saving the store "{}" to the database'.format(name)}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {'message': 'an error occured deleting this store'}, 500

            return {'message': "the store '{}' was deleted from the database".format(name)}, 201
        return {'message': "The '{}' store was not found".format(name)}, 404

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
