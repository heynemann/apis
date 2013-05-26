#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import logging

from ujson import loads, dumps
import tornado.web
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from geo.handlers import BaseHandler

ONE_MINUTE_LENGTH = 1.853


class LocationHandler(BaseHandler):

    @tornado.web.asynchronous
    def get(self):
        secret = self.request.headers.get('X-Mashape-Proxy-Secret', None)
        if not self.application.config.LOCAL and (not secret or secret != self.application.config.MASHAPE_LOCATIONS_SECRET):
            logging.warn("Someone trying to access the API directly (secret passed in: %s)." % secret)
            self._error(status=404)
            return

        latitude = float(self.get_argument('lat'))
        longitude = float(self.get_argument('long'))
        radius = float(self.get_argument('radius', 50))

        radius = radius / 1000 / ONE_MINUTE_LENGTH

        language = self.get_argument('language', 'en')

        self.set_header('Content-Type', 'text/javascript')

        self.query_dbpedia("""
            PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
            SELECT ?subject ?label ?lat ?long WHERE {
            ?subject geo:lat ?lat.
            ?subject geo:long ?long.
            ?subject rdfs:label ?label.
            FILTER(
                ?lat - (%(latitude).8f) <= %(tolerance).8f && (%(latitude).8f) - ?lat <= %(tolerance).8f &&
                ?long - (%(longitude).8f) <= %(tolerance).8f && (%(longitude).8f) - ?long <= %(tolerance).8f &&
                lang(?label) = "%(language)s"
            )
            } LIMIT 20
        """ % {
            'latitude': latitude,
            'longitude': longitude,
            'tolerance': radius,
            'language': language
        })

    def query_dbpedia(self, q):
        epr = "http://dbpedia.org/sparql"
        params = {'query': q}
        params = urllib.urlencode(params)

        req = HTTPRequest("%s?%s" % (epr, params), headers={
            'Accept': 'application/json'
        }, follow_redirects=False)

        http_client = AsyncHTTPClient()
        http_client.fetch(req, self.handle_dbpedia_response)

    def handle_dbpedia_response(self, response):
        if response.error:
            self._error(400)
        try:
            results = loads(response.body)
            items = []
            for result in results['results']['bindings']:
                items.append({
                    'label': result['label']['value'],
                    'longitude': float(result['long']['value']),
                    'latitude': float(result['lat']['value'])
                })

            self.render_response(dumps(items))
        finally:
            self.finish()
