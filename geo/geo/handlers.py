#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import logging
import traceback

import tornado.web

from geo import __version__


class BaseHandler(tornado.web.RequestHandler):
    def _error(self, status, msg=None):
        self.set_status(status)
        self.finish()

    def render_response(self, response):
        callback = self.get_arguments('callback', None)

        if callback:
            self.write('%s(%s)' % (callback, response))
        else:
            self.write(response)

    def _handle_request_exception(self, e):
        try:
            exc_info = sys.exc_info()
            msg = traceback.format_exception(exc_info[0], exc_info[1], exc_info[2])

            extra = {
                'apis-geo-version': __version__
            }

            extra.update(self.request.headers)

            cookies = {}
            for cookie in extra['Cookie'].split(';'):
                values = cookie.split('=')
                key, val = values[0], "".join(values[1:])
                cookies[key] = val
            extra['Cookie'] = cookies

            data = {
                'sentry.interfaces.Http': {
                    'url': self.request.full_url(),
                    'method': self.request.method,
                    'data': self.request.arguments,
                    'body': self.request.body,
                    'query_string': self.request.query,
                    'cookies': self.request.headers.get('Cookie', None),
                    'headers': dict(self.request.headers),
                },
                'sentry.interfaces.User': {
                    'ip': self.request.remote_ip,
                    'real-ip': self.request.headers.get('X-Real-IP', self.request.remote_ip)
                },
                'modules': self.application.modules
            }
            self.application.sentry.captureException(exc_info, extra=extra, data=data)
        finally:
            del exc_info

        logging.error('ERROR: %s' % "".join(msg))
        self.send_error(500)
