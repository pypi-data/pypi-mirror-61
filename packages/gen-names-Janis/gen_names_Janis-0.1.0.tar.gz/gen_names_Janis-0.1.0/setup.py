#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='gen_names_Janis',
    version='0.1.0',
    author='JK company PLC',
    author_email='jkarasa@gmail.com',
    package=find_packages(),
    include_package_data=True,
    description='Super useful library',
    install_requires=['names'],

    scripts=['Setup_Janis/gen_names_Janis.py', 'bin/gen_names_Janis.sh']


)
