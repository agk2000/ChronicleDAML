#modified from https://developers.google.com/analytics/devguides/reporting/core/v4/basics
from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import os, ast

class Analytics(Resource):
    KEY_FILE_LOCATION1 = os.getenv('chronicletest') #get from .env file
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    VIEW_ID = os.getenv('viewid') #viewid for analytics page

    def initialize_analyticsreporting(): #initializes Analytics Reporting API V4 service object
      KEY_FILE_LOCATION = ast.literal_eval(Analytics.KEY_FILE_LOCATION1) #convert string to dict
      credentials = ServiceAccountCredentials.from_json_keyfile_dict(KEY_FILE_LOCATION, Analytics.SCOPES)
      analytics = build('analyticsreporting', 'v4', credentials=credentials) #Build service object
      return analytics

    def get_report(analytics, name, date_start, date_end, *args):
      return analytics.reports().batchGet(
          body={
            'reportRequests': [
            {
              'viewId': Analytics.VIEW_ID,
              'dateRanges': [{'startDate': date_start, 'endDate': date_end}],
              'metrics': [{'expression': arg} for arg in args],
              'dimensions': [{'name': 'ga:pageTitle'}],
              'dimensionFilterClauses': [
                {
                    'filters': [
                        {
                            'dimensionName': 'ga:pageTitle',
                            'operator': 'BEGINS_WITH',
                            'expressions': [name]
                        }
                    ]
                }
              ]
            }]
          }
      ).execute()

    def clean_response(response):
        """Parses and prints the Analytics Reporting API V4 response.
        Args: response: An Analytics Reporting API V4 response.
        """
        article_list =  []
        for report in response.get('reports', []):
            columnHeader = report.get('columnHeader', {})
            dimensionHeaders = columnHeader.get('dimensions', [])
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

            for row in report.get('data', {}).get('rows', []):
                dimensions = row.get('dimensions', [])
                dateRangeValues = row.get('metrics', [])
                new_dict = {}
                for header, dimension in zip(dimensionHeaders, dimensions):
                    new_dict["header"] = dimension
                for i, values in enumerate(dateRangeValues):
                    for metricHeader, value in zip(metricHeaders, values.get('values')):
                        new_dict[metricHeader.get('name')] = value
                article_list.append(new_dict)
        return article_list

    @jwt_required()
    def get(self, name):
        analytics = Analytics.initialize_analyticsreporting()
        if name == 'searchhead':
            content = request.headers.get('title')
        else:
            content = request.args.get('title')
        start_date = request.args.get('startdate', default = '2008-01-01')
        end_date = request.args.get('enddate', default = 'today')
        parameters = request.args.getlist('parameters')
        response = Analytics.get_report(analytics, content, start_date, end_date, *parameters)
        return response


class AnalyticsClean(Resource):
    @jwt_required()
    def get(self, name):
        analytics = Analytics.initialize_analyticsreporting()
        if name == 'searchhead':
            content = request.headers.get('title')
        else:
            content = request.args.get('title')
        start_date = request.args.get('startdate', default = '2008-01-01')
        end_date = request.args.get('enddate', default = 'today')
        parameters = request.args.getlist('parameters')
        response = Analytics.get_report(analytics, content, start_date, end_date, *parameters)
        cleaned_response = Analytics.clean_response(response)
        return cleaned_response
