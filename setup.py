# -*- coding: UTF-8 -*-
"""Setup script"""

from distutils.core import setup

T_VARS = {}
with open('.PROJINFO') as vars_file:
    for line in vars_file:
        key, value = line.partition('=')[::2]
        T_VARS[key.strip()] = value.strip()

setup(
    name=T_VARS['NAME'],
    version=T_VARS['VERSION'],
    packages=['eljef', 'eljef.core'],
    url='https://github.com/eljef/eljef_core',
    license='LGPLv2.1',
    author='Jef Oliver',
    author_email='jef.oliver@intel.com',
    description='Core Functions for various utilities written by Jef Oliver',
    install_requires=['yaml', 'xmltodict']
)
