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
        secret = self.request.headers.get('X-Mashape-Proxy-Secret', None)
        if not self.application.config.LOCAL and (not secret or secret != self.application.config.MASHAPE_SECRET):
            logging.warn("Someone trying to access the API directly.")
            self._error(status=404)
            return

        header_key = 'X-Real-IP'
        ip_address = header_key in self.request.headers and self.request.headers[header_key] or self.request.remote_ip
        logging.info("HEADERS: %s" % self.request.headers)

        ip_address = self.get_argument('ip', ip_address)
        ip_address = ip_address

        geo = GeoLocation(ip_address, geo_db_contents=self.geo_db_contents)

        self.set_header('Content-Type', 'text/javascript')

        if geo.success:
            self.render_response(dumps(geo.as_dict()))
        else:
            logging.info('IP address: %s NOT FOUND' % ip_address)
            self.render_response('''{ ip: '%s' }''' % ip_address)

        self.finish()
