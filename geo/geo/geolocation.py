#!/usr/bin/python
# -*- coding: utf-8 -*-

from json import dumps

import tornado.web
import logging

from geo.handlers import BaseHandler
from geo.models import GeoLocation


class GeoHandler(BaseHandler):

    def initialize(self, geo_db_contents):
        self.geo_db_contents = geo_db_contents

    @tornado.web.asynchronous
    def get(self):
        header_key = 'X-Real-IP'
        ip_address = header_key in self.request.headers and self.request.headers[header_key] or self.request.remote_ip

        ip_address = self.get_argument('ip', [ip_address])
        ip_address = ip_address[0]

        geo = GeoLocation(ip_address, geo_db_contents=self.geo_db_contents)

        self.set_header('Content-Type', 'text/javascript')

        if geo.success:
            self.render_response(dumps(geo.as_dict()))
        else:
            logging.info('IP address: %s NOT FOUND' % ip_address)
            self.render_response('')

        self.finish()
