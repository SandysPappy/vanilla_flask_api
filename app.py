# Not using databases yet
# using an in-memory database, aka a list.
# So just focusing on JSON rn

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from db import db

from resources.user import UserRegister
from resources.item import ItemList, Item
from resources.store import Store, StoreList

app = Flask(__name__)

# To know when an object was changed but not saved to the database,
# the extention flask_sqlalchemy was tracking everything changed
#
# However, now sql SQLAlchemy itself tracks modifications, so we turn
# flask's modification tracker off here

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # change other sqls here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DO NOT PUBLISH THIS KEY ONLINE
# DO NOT COMMIT THIS SECRET KEY TO A GITHUB REPO
app.secret_key = 'super_secret key here'
api = Api(app)

# creates the tables if they don't exist already
# each resource is found in the previous resource imports
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # JWT creates endpoint /auth
# when we call /auth, it send it a username and password, and sends it
# to the authenticate password. We find the correct user object using
# that username, and compare the sent password to the one in the database.
# If they match, the user is returned as a jw token? idk

# Now student is accessable via the api
# http://127.0.0.1:5000/item/Idk_insert_custom_name_here
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# if app.py is imported, the flask app is not ran
if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
