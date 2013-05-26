#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from os.path import expanduser, dirname
import logging
import traceback

import tornado.web
from raven import Client

from geo.config import Config
from geo.utils import FakeSentry, get_modules
from geo import __version__
from geo.healthcheck import HealthCheckHandler
from geo.geolocation import GeoHandler
from geo.location import LocationHandler


class GeoApp(tornado.web.Application):
    def __init__(self, conf_file=None, main_loop=None, debug=False):
        lookup_paths = [
            os.curdir,
            expanduser('~'),
            '/etc/',
            dirname(__file__)
        ]
        self.config = Config.load(conf_file, conf_name='geo.conf', lookup_paths=lookup_paths)

        if self.config.USE_SENTRY:
            self.sentry = Client(self.config.SENTRY_DSN_URL)
        else:
            self.sentry = FakeSentry(self.config.SENTRY_DSN_URL)

        self.modules = get_modules()
        self.debug = debug

    def initialize(self):
        geo_db_content = None
        with open(self.config.GEO_DATABASE_PATH) as geo_db_file:
            geo_db_content = geo_db_file.read()

        handlers = [
            (r'/healthcheck(?:/|\.html)?', HealthCheckHandler),
            (r'/?', GeoHandler, {'geo_db_contents': geo_db_content}),
            (r'/locations/?', LocationHandler),
        ]

        options = {}
        if self.debug:
            options['debug'] = True

        super(GeoApp, self).__init__(handlers, **options)

    def report_error(self):
        try:
            exc_info = sys.exc_info()
            msg = "".join(traceback.format_exception(exc_info[0], exc_info[1], exc_info[2]))

            extra = {
                'apis-geo-version': __version__
            }

            data = {
                'modules': self.modules
            }
            self.sentry.captureException(exc_info, extra=extra, data=data)
        finally:
            del exc_info

        logging.error('ERROR:\n%s' % msg)
