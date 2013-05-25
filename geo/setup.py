#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from geo import __version__

tests_require = [
]

setup(
    name='geo',
    version=__version__,
    description='geo is an api to find geolocation information',
    long_description='''
geo is an api to find geolocation information
''',
    keywords='geo',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='http://github.com/heynemann/apis/',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(),
    install_requires=[
        'derpconf',
        'tornado',
        'raven',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            'apis-geo=geo.server:main',
        ],
    },
)
