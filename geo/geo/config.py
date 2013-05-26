#!/usr/bin/python
# -*- coding: utf-8 -*-

from derpconf.config import Config

Config.define('GEO_DATABASE_PATH', './geo/db/GeoLiteCity.dat', 'Geo database path', 'GEO')
Config.define('MASHAPE_GEO_SECRET', 'DgEiRl57EA1uVvyLCVZOdr4gUhB4kt', 'Mashape Secret', 'Security')
Config.define('MASHAPE_LOCATIONS_SECRET', 'n5PV3vdyEA10OW3I0AS2C0qipoAhMz', 'Mashape Secret', 'Security')

Config.define('LOCAL', True, 'am I running locally?', 'Security')

Config.define('USE_SENTRY', False, 'Should we user sentry?', 'Sentry')
Config.define('SENTRY_DSN_URL', '', 'Sentry DSN', 'Sentry')
