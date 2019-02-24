import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

# CRUD
# Most API's follow the CRUD method
# - Create - POST
# - Read - GET
# - Update - PUT
# - Delete - DELETE

# EVERY RESOURCE HAS TO BE A CLASS
class Item(Resource):
    parser = reqparse.RequestParser()
    # ensure that we only parse requests by price
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)

        if item:
            return item

        return {"message": "Item not found"}, 404

    # POPULAR INTERVIEW QUESTION:
    # "What's the  most popular http status code? 404 (NOT 200!)"

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):  # this has to have the same method signature!
        # ERROR FIRST APPROACH
        if self.find_by_name(name):
            # 400: SOMETHING WENT WRONG WITH THE REQUEST
            return ({"message": f"An item with name '{name}' already exists"},
                    400)

        # data = request.get_json() REPLACED BY .parse_args()
        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            # 500: INTERNAL SERVER ERROR
            return {"message": "An error occurred inserting item."}, 500

        return item, 201  # lets client (application) know this happened
        # 201 code is a CREATED status

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        # check if item exists
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting item."}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating item."}, 500

        return updated_item


    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}
