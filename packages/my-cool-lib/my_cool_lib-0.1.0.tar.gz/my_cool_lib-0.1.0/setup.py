# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='my_cool_lib',
    version='0.1.0',
    author='SomeCompany PLC',
    author_email='dev@example.com',
    packages=find_packages(),
    include_package_data=True,
    description='Super useful library',
    url='https://github.com',
    install_requires=['names'],
    scripts=['get_names/gen_names.py', 'bin/get_names.bat']
)