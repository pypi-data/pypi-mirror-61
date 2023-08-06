#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
import os

top, _ = os.path.split(__file__)
with open(os.path.join(top, 'VERSION'), 'r') as fin:
    version = fin.read().strip() + '+local'
version = '0.3.1'.format(version=version)

setup(
    name='pe_tools',
    version=version,

    url='https://github.com/avast/pe_tools',
    maintainer='Martin Vejnár',
    maintainer_email='martin.vejnar@avast.com',

    packages=['pe_tools'],
    install_requires=['grope'],

    entry_points={
        'console_scripts': [
            'peresed = pe_tools.peresed:main',
            ],
        }
    )
