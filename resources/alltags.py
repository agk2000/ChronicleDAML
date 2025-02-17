from flask_restful import Resource
from flask_jwt import jwt_required
import jwt as jwt_s
from datetime import datetime, timedelta
import requests, os

class AllTags(Resource):
    @jwt_required()
    def get(self):
        private_key1 = os.getenv('private_key1') #get from .env file
        public_key1 = os.getenv('public_key1') #get from .env file
        encoded_jwt = jwt_s.encode({'aud': 'https://dtc.ceo.getsnworks.com/', 'pk': public_key1,'iat': datetime.now(), 'exp': datetime.now() + timedelta(seconds=300)}, private_key1, algorithm='HS256')
        encoded_jwt_str = encoded_jwt.decode('UTF-8')
        header = {'Authorization': 'Bearer ' + encoded_jwt_str}
        r = requests.get('https://dtc.ceo.getsnworks.com/v3/tag', headers = header)
        count = r.json().get('total_pages')
        item_list =  []
        for i in range(1, count+1):
            payload = {'page':str(i)}
            r = requests.get('https://dtc.ceo.getsnworks.com/v3/tag', headers = header, params=payload)
            newlist = r.json().get('items', [])
            item_list.extend(newlist)
        return item_list
