#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name = 'django-email-authentication',
    version = '0.1.1',
    author = 'ted kaemming',
    author_email = 'ted.kaemming@workshop33.com',
    url = 'http://github.com/workshop33/django-email-authentication',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    zip_safe = False,
)
