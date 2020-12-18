# -*- coding: UTF-8 -*-
"""Setup script"""

from setuptools import setup

setup(
    author='Jef Oliver',
    author_email='jef@eljef.me',
    description='Core functions for various utilities written by Jef Oliver',
    install_requires=['colorlog', 'PyYAML', 'xmltodict'],
    license='LGPLv2.1',
    name='eljef_core',
    packages=['eljef.core'],
    python_requires='>=3.8',
    url='https://github.com/eljef/python_eljef_core',
    version='1.4.1',
    zip_safe=False,
)
