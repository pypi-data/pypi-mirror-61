#!/usr/bin/python
# -*- cding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name = 'gen_name',
    version = '0.1.0',
    author ='Ellgreco',
    author_email = 'ellgreco@protonmail.com',
    include_packages_data = True,
    description = 'Super useful library',
    url ='https://github.com/treyhunner/names',
    keywors = 'random names',
    packages = find_packages(),
    scripts = ['gen_names/gen_names_ellgreco.py', 'bin/gen_names_ellgreco.bat'],
    install_requires = ['name']
)