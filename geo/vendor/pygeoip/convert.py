#!/usr/bin/python
# -*- coding: utf-8 -*-

def convert():
    contents = open('fips_include.txt').read().split('\n')

    print "REGIONS = {"

    last_country = ""
    first = True

    for index, line in enumerate(contents):
        if not line:
            continue

        values = line.split(',')
        next_line_values = ['', '', '']
        if not index == len(contents) - 1:
            next_line_values = contents[index + 1].split(',')

        country, region_code, region_name = values[0], values[1], ','.join(values[2:])

        if country != last_country:
            if not first:
                print '    },'
            print '    u"%s": {' % country

            first = False

        if next_line_values[0] != country:
            print '        u"%s": u%s' % (region_code, region_name)
        else:
            print '        u"%s": u%s,' % (region_code, region_name)

        last_country = country

    print "    }"
    print "}"

if __name__ == '__main__':
    convert()
