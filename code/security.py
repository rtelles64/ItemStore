# Contains a few important functions
from user import User
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = User.find_by_username(username)

    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):  # unique to Flask JWT
    user_id = payload['identity']
    return User.find_by_id(user_id)