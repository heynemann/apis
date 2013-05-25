#!/usr/bin/python
# -*- coding: utf-8 -*-

from derpconf.config import Config

Config.define('GEO_DATABASE_PATH', './geo/db/GeoLiteCity.dat', 'Geo database path', 'GEO')

Config.define('USE_SENTRY', False, 'Should we user sentry?', 'Sentry')
Config.define('SENTRY_DSN_URL', '', 'Sentry DSN', 'Sentry')
