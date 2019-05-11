# -*- coding: UTF-8 -*-
"""Setup script"""

import sys
from setuptools import setup

if sys.version_info[0] < 3:
    raise Exception('ElJef tools only support python version 3.6 or higher.')
if sys.version_info[0] > 3 and sys.version_info[1] < 6:
    raise Exception('ElJef tools only support python version 3.6 or higher.')

setup(
    author='Jef Oliver',
    author_email='jef@eljef.me',
    description='Core functions for various utilities written by Jef Oliver',
    install_requires=['colorlog', 'pyaml', 'xmltodict'],
    license='LGPLv2.1',
    name='eljef_core',
    packages=['eljef.core'],
    python_requires='>=3.6',
    url='https://github.com/eljef/python_eljef_core',
    version='0.0.16',
    zip_safe=False,
)
