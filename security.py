from werkzeug.security import safe_str_cmp
from models.user import User
import os

users = []
for i in range(5):
    username = os.getenv('username' + str(i+1))
    password = os.getenv('password' + str(i+1))
    users.append(User(i+1,  username, password))

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)
