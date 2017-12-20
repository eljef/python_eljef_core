# -*- coding: UTF-8 -*-
"""Setup script"""

import sys
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
    raise Exception('ElJef tools only support python version 3.6 or higher.')
if sys.version_info[0] > 3 and sys.version_info[1] < 6:
    raise Exception('ElJef tools only support python version 3.6 or higher.')

T_VARS = {}
with open('.PROJINFO') as vars_file:
    for line in vars_file:
        key, value = line.partition('=')[::2]
        T_VARS[key.strip()] = value.strip()

setup(
    name=T_VARS['NAME'],
    version=T_VARS['VERSION'],
    packages=find_packages(),
    url='https://github.com/eljef/python_eljef_core',
    license='LGPLv2.1',
    author='Jef Oliver',
    author_email='jef@eljef.me',
    description='Core Functions for various utilities written by Jef Oliver',
    install_requires=['pyyaml', 'xmltodict'],
    python_requires='>=3.6'
)
