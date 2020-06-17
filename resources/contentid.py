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


class ContentIDClean(Resource):
    def clean_response(unclean_response):
        copy_variables = ['id', 'uuid', 'type', 'title', 'slug', 'published_at', 'version', 'content', 'abstract']
        cleaned_response = {}
        for article in unclean_response:
            for variable in copy_variables:
                cleaned_response[variable] = article.get(variable)

            unclean_author_list =  article.get('authors', [])
            clean_author_list = []
            for content_author in unclean_author_list:
                clean_author_list.append(content_author.get('name'))
            cleaned_response['authors'] = clean_author_list

            unclean_tag_list = article.get('tags', [])
            clean_tag_list = []
            for content_tag in unclean_tag_list:
                clean_tag_list.append(content_tag.get('name'))
            cleaned_response['tags'] = clean_tag_list

        return cleaned_response

    @jwt_required()
    def get(self, name):
        init_response = ContentID.get(self, name)
        cleaned_response = ContentIDClean.clean_response(init_response)
        return cleaned_response


class ContentIDTags(Resource):
    def clean_tags(unclean_response):
        cleaned_tags = []
        for article in unclean_response:
            unclean_tag_list = article.get('tags', [])
            for content_tag in unclean_tag_list:
                cleaned_tags.append(content_tag.get('name'))
        return cleaned_tags

    @jwt_required()
    def get(self, name):
        init_response = ContentID.get(self, name)
        cleaned_response = ContentIDTags.clean_tags(init_response)
        return cleaned_response


class ContentIDAuthors(Resource):
    def clean_authors(unclean_response):
        cleaned_authors = []
        for article in unclean_response:
            unclean_author_list = article.get('authors', [])
            for content_author in unclean_author_list:
                cleaned_authors.append(content_author.get('name'))
        return cleaned_authors

    @jwt_required()
    def get(self, name):
        init_response = ContentID.get(self, name)
        cleaned_response = ContentIDAuthors.clean_authors(init_response)
        return cleaned_response
