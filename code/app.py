# This template provides a RESTful structure
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

# NOTE: we no longer use jsonify since flask_restful does it for us

app = Flask(__name__)
# NOTE: if this is a production API, the secret_key should be hidden
app.secret_key = "81h2459gpasiubdglkqwy97ryqhou!@##%@#^"
api = Api(app)  # easily add resources to our API

jwt = JWT(app, authenticate, identity)  # /auth

# ADD RESOURCE (with route)
# http://127.0.0.1:5000/item/name
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':  # prevents from running app.py if it is an import
    app.run(port=5000, debug=True)  # port 5000 is the default but it's nice to
    #                                  get practice
