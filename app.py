from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
import requests, os
from security import authenticate, identity

from resources.analyticstitle import Analytics
from resources.allauthors import AllAuthors
from resources.authorid import AuthorID
from resources.tagcontent import TagContent
from resources.contentid import ContentID
from resources.allcontent import AllContent
from resources.alltags import AllTags
from resources.authorcontent import Author

app = Flask(__name__)
app.secret_key = os.getenv('secret_key') #get from .env file
api = Api(app)

jwt = JWT(app, authenticate, identity)


"""/analyticstitle/<title>
    #get analytics for any article by title
    # Arguments: query string with parameter keys title, startdate, enddate, parameters*
        #Default values are startdate:2008-01-1, enddate:today, parameters:['ga:timeOnPage']
        #startdate must be after 2005-01-01
        #startdate can also be '7daysAgo'
    # Response: json with all page analytics deata for the given metrics"""
api.add_resource(Analytics, '/analyticstitle/<string:name>')

"""/authorid/<author_uuid>
    #gets all author item info given uuid
    # Arguments: author uuid
    # Response: author item json with author id, uuid, slug, name, email, tagline, description, status of author, etc."""
api.add_resource(AuthorID, '/authorid/<string:name>')

"""/author/<author_name>
    #gets all articles (content items) given author
    # Arguments: url encoded author name
    # Response: content item json with all articles by a given author (content id, uuid, title, slug, type, abstract, content, etc.)"""
api.add_resource(Author, '/authorcontent/<string:name>')

"""#/contentid/<content_uuid>
    #gets content item given content uuid
    # Arguments: content uuid
    # Response: content item json with all relevant info (content id, uuid, title, abstract, content, author, creation/publish date, etc.)"""
api.add_resource(ContentID, '/contentid/<string:name>')

"""#/tagcontent/<tag_name>
    #gets content item given tags
    # Arguments: tag name
    # Response: content item jsons"""
api.add_resource(TagContent, '/tagcontent/<string:name>')

"""#/allauthors
    #gets all author items
    # Arguments:
    # Response: all author items"""
api.add_resource(AllAuthors, '/allauthors')

"""#/allcontent
    #gets all content items
    # Arguments:
    # Response: all author items"""
api.add_resource(AllContent, '/allcontent')

"""#/alltags
    #gets all tag items
    # Arguments:
    # Response: all tag items"""
api.add_resource(AllTags, '/alltags')


"""
A few tags
    1: "Top Stories"
    2: "Sports"
    3: "Entertainment"
    4: "Opinion"
    5: "news"
    12: "basketball"
    17: "letter to the editor"
    19: "Academics"
    20: "student life"
    34: "Column"
    59: "topstory"
    71: "newsletter-top"
    88: "editors note"
    6386: "Zion Williamson"
    6501: "topstory-featured"
    6513: "coronavirus"
"""


if __name__ == '__main__':
    app.run(debug=True)
