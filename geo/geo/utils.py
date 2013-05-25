#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import traceback
import pkgutil
import pkg_resources


class FakeSentry(object):
    def __init__(self, dsn):
        self.dsn = dsn

    def captureException(self, exc_info, *args, **kw):
        logging.error(''.join(traceback.format_exception(exc_info[0], exc_info[1], exc_info[2])))


def get_modules():
    resolved = {}
    modules = [mod[1] for mod in tuple(pkgutil.iter_modules())]
    for module in modules:
        try:
            res_mod = pkg_resources.get_distribution(module)
            if res_mod is not None:
                resolved[module] = res_mod.version
        except pkg_resources.DistributionNotFound:
            pass

    return resolved

intab = u"áãàäâéèêëíìïîóòõöôúùüûñç"
outab = u"aaaaaeeeeiiiiooooouuuunc"
translate_table = dict((ord(intab[i]), outab[i]) for i in range(len(intab)))


def translate_accents(s):
    return s.translate(translate_table)


def urlize(word):
    return word.translate(translate_table).replace("'", '').replace('"', '').replace(' ', '-')
