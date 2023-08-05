#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='get_names_grizzy',
    version='0.1.1',
    author='Lukasz Nowak',
    author_email='lukasz.nowak1@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    description='My first library',
    url='http://google.pl/',
    keywords='names and len',
    install_requires=['names'],
    scripts=['gen_names_grizzy/gen_names_grizzy.py', 'bin/gen_names_grizzy.bat']
)