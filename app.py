from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
import requests, os
from security import authenticate, identity
from datetime import timedelta

from resources.analyticstitle import Analytics, AnalyticsClean
from resources.allauthors import AllAuthors
from resources.authorid import AuthorID, AuthorIDClean
from resources.tagcontent import TagContent
from resources.contentid import ContentID, ContentIDClean, ContentIDTags, ContentIDAuthors
from resources.allcontentfifty import AllContentFifty, AllContentFiftyClean
from resources.alltags import AllTags
from resources.authorcontent import Author, AuthorClean

app = Flask(__name__)
app.secret_key = os.getenv('secret_key') #get from .env file
api = Api(app)

jwt = JWT(app, authenticate, identity)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=21600)

"""/analyticstitle/<title>
    #get analytics for any article by title
    # Arguments: query string with parameter keys title, startdate, enddate, parameters*
        #searchyb allows title to be passed as header instead
        #Default values are startdate:2008-01-1, enddate:today, parameters:['ga:timeOnPage']
        #startdate must be after 2005-01-01
        #startdate can also be '7daysAgo'
    # Response: json with all page analytics deata for the given metrics"""
api.add_resource(Analytics, '/analyticstitle/<string:name>')
api.add_resource(AnalyticsClean, '/analyticstitle/clean/<string:name>') #cleaned version

"""/authorid/<author_uuid>
    #gets all author item info given uuid
    # Arguments: author uuid
    # Response: author item json with author id, uuid, slug, name, email, tagline, description, status of author, etc."""
api.add_resource(AuthorID, '/authorid/<string:name>')
api.add_resource(AuthorIDClean, '/authorid/clean/<string:name>') #just name of author

"""/author/<author_name>
    #gets all articles (content items) given author
    # Arguments: url encoded author name
    # Response: content item json with all articles by a given author (content id, uuid, title, slug, type, abstract, content, etc.)"""
api.add_resource(Author, '/authorcontent/<string:name>')
api.add_resource(AuthorClean, '/authorcontent/clean/<string:name>')

"""#/contentid/<content_uuid>
    #gets content item given content uuid
    # Arguments: content uuid
    # Response: content item json with all relevant info (content id, uuid, title, abstract, content, author, creation/publish date, etc.)"""
api.add_resource(ContentID, '/contentid/<string:name>')
api.add_resource(ContentIDClean, '/contentid/clean/<string:name>') #just id, uuid, type, content, title, slug, version, abstract, content, published_at, authors, keywords
api.add_resource(ContentIDTags, '/contentid/cleantags/<string:name>') #just tags of content
api.add_resource(ContentIDAuthors, '/contentid/cleanauthors/<string:name>') #just authors of content

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
    #gets page of fifty content items
    # Arguments:
    # Response: fifty content items by page number"""
api.add_resource(AllContentFifty, '/allcontentfifty/<string:name>')
api.add_resource(AllContentFiftyClean, '/allcontentfifty/clean/<string:name>')

"""#/alltags
    #gets all tag items
    # Arguments:
    # Response: all tag items"""
api.add_resource(AllTags, '/alltags')


if __name__ == '__main__':
    app.run(debug=True)
