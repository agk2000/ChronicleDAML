from flask_restful import Resource
from flask_jwt import jwt_required
import jwt as jwt_s
from datetime import datetime, timedelta
import requests, os

class AllContentFifty(Resource):
    @jwt_required()
    def get(self,  name):
        private_key1 = os.getenv('private_key1') #get from .env file
        public_key1 = os.getenv('public_key1') #get from .env file
        encoded_jwt = jwt_s.encode({'aud': 'https://dtc.ceo.getsnworks.com/', 'pk': public_key1,'iat': datetime.now(), 'exp': datetime.now() + timedelta(seconds=300)}, private_key1, algorithm='HS256')
        encoded_jwt_str = encoded_jwt.decode('UTF-8')
        header = {'Authorization': 'Bearer ' + encoded_jwt_str}
        payload = {'page':name}
        r = requests.get('https://dtc.ceo.getsnworks.com/v3/content', headers = header, params=payload)
        return r.json()

class AllContentFiftyClean(Resource):
    def clean_response(unclean_response):
        copy_variables = ['id', 'uuid', 'type', 'title', 'slug', 'created_at', 'modified_at', 'published_at', 'version', 'abstract', 'content']
        cleaned_response = {}
        for variable in copy_variables:
            cleaned_response[variable] = unclean_response.get(variable)

        unclean_tag_list = unclean_response.get('tags', [])
        clean_tag_list = []
        for content_tag in unclean_tag_list:
            clean_tag_list.append(content_tag.get('name'))
        cleaned_response['tags'] = clean_tag_list
        cleaned_response['keywords'] = unclean_response.get('keywords')

        return cleaned_response

    @jwt_required()
    def get(self,  name):
        init_response = (AllContentFifty.get(self, name)).get('items', [])
        cleaned_content_list = []
        for item in init_response:
            cleaned_dict = AllContentFiftyClean.clean_response(item)
            cleaned_content_list.append(cleaned_dict)

        clean_dict = {}
        clean_dict['items'] = cleaned_content_list

        return clean_dict
