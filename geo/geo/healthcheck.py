#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

from geo.handlers import BaseHandler


class HealthCheckHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write('WORKING')
        self.finish()
