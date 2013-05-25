#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

import pygeoip
from pygeoip.regions import get_region_name

from geo.utils import urlize


class GeoLocation(object):
    def __init__(self, ip, db_path=None, geo_db_contents=None):
        self.ip = ip

        self.success = None
        self.country = None
        self.country_code = None
        self.state = None
        self.abbrev_state = None
        self.city = None
        self.latitude = None
        self.longitude = None
        self.db_path = db_path
        self.geo_db_contents = geo_db_contents

        self.find_geo_location()

    def find_geo_location(self):
        gi = pygeoip.GeoIP(self.db_path, db_contents=self.geo_db_contents)
        try:
            self.success = True
            result = gi.record_by_addr(self.ip)

            if 'country_name' in result:
                self.country = unicode(result['country_name'])
                self.country_code = result['country_code']

            if 'region_name' in result:
                self.state = get_region_name(result['country_code'], result['region_name'])
                self.region_name = result['region_name']

            if 'city' in result:
                self.city = result['city'].decode('ISO-8859-1').encode('utf8')

            if 'latitude' in result:
                self.latitude = result['latitude']

            if 'longitude' in result:
                self.longitude = result['longitude']

        except Exception, err:
            self.success = False
            logging.info("Geolocation for ip %s could not be retrieved. Error: %s" % (self.ip, str(err)))

    def as_dict(self):
        geolocation = {
            "country": {
                "name": self.country,
                "code": self.country_code,
            },
            "state": {
                "name": self.state,
                "code": self.state and urlize(self.region_name.decode('utf-8')) or None
            },
            "city": {
                "name": self.city,
                "code": self.city and urlize(self.city.decode('utf-8').lower()) or None
            },
            "latitude": self.latitude,
            "longitude": self.longitude
        }

        geolocation['ip'] = self.ip

        return geolocation
