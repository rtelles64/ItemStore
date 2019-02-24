# adds ability to retrieve User objects from the database
import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod  # since we don't use self anywhere but only the class name
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')  # initialize connection
        cursor = connection.cursor()  # initialize cursor

        query = "SELECT * FROM users WHERE username=?"
        # NOTE: execute() parameters ALWAYS have to be in the form of a tuple
        #       even if there is only one
        result = cursor.execute(query, (username,))  # get result set
        row = result.fetchone()  # just get first row out of result set
        #                          if there are no rows, this returns None

        if row:
            # RECALL unpacking arguments!
            user = cls(*row)  # cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()  # close connection

        return user  # either User object or None

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            # RECALL unpacking arguments!
            user = cls(*row)  # cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()

        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()  # get data
    parser.add_argument('username',  # only get username
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    parser.add_argument('password',  # and password
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        # use data retrieved from parser
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # NULL for id position since it auto increments
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created succesffuly."}, 201  # CREATED
