#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

import tornado.ioloop
from tornado.httpserver import HTTPServer

from geo.app import GeoApp

LOGS = {
    0: 'error',
    1: 'warning',
    2: 'info',
    3: 'debug'
}


def run_app(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default="9999", help="Port to start the server with.")
    parser.add_argument('--bind', '-b', default="0.0.0.0", help="IP to bind the server to.")
    parser.add_argument('--conf', '-c', default=None, help="Path to configuration file.")
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Log level: v=warning, vv=info, vvv=debug.')
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Indicates whether to run wight api in debug mode.')
    options = parser.parse_args(args)

    log_level = LOGS[options.verbose].upper()
    logging.basicConfig(level=getattr(logging, log_level), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    main_loop = tornado.ioloop.IOLoop.instance()

    application = GeoApp(options.conf, main_loop=main_loop)

    try:
        application.initialize()

        server = HTTPServer(application)
        server.bind(options.port, options.bind)
        server.start(1)

        print '-- apis-geo started listening in %s:%d --' % (options.bind, options.port)
        try:
            main_loop.start()
        except KeyboardInterrupt:
            print
            print '-- apis-geo closed by user interruption --'
    except Exception:
        application.report_error()


def main():
    run_app()


if __name__ == '__main__':
    main()
