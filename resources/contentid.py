from flask_restful import Resource
from flask_jwt import jwt_required
import jwt as jwt_s
from datetime import datetime, timedelta
import requests, os

class ContentID(Resource):
    @jwt_required()
    def get(self, name):
        private_key1 = os.getenv('private_key1') #get from .env file
        public_key1 = os.getenv('public_key1') #get from .env file
        encoded_jwt = jwt_s.encode({'aud': 'https://dtc.ceo.getsnworks.com/', 'pk': public_key1,'iat': datetime.now(), 'exp': datetime.now() + timedelta(seconds=300)}, private_key1, algorithm='HS256')
        encoded_jwt_str = encoded_jwt.decode('UTF-8')
        header = {'Authorization': 'Bearer ' + encoded_jwt_str}
        r = requests.get('https://dtc.ceo.getsnworks.com/v3/content/'+name, headers = header)
        return r.json()
