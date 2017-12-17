# -*- coding: UTF-8 -*-
"""Setup script"""

from setuptools import setup, find_packages

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
    install_requires=['pyyaml', 'xmltodict']
)
