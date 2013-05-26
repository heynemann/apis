#!/usr/bin/python
# -*- coding: utf-8 -*-

from derpconf.config import Config

Config.define('GEO_DATABASE_PATH', './geo/db/GeoLiteCity.dat', 'Geo database path', 'GEO')
Config.define('MASHAPE_SECRET', 'DgEiRl57EA1uVvyLCVZOdr4gUhB4kt', 'Mashape Secret', 'Security')
Config.define('LOCAL', True, 'am I running locally?', 'Security')

Config.define('USE_SENTRY', False, 'Should we user sentry?', 'Sentry')
Config.define('SENTRY_DSN_URL', '', 'Sentry DSN', 'Sentry')
