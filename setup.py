# -*- coding: UTF-8 -*-
"""Setup script"""

from setuptools import setup

setup(
    author='Jef Oliver',
    author_email='jef@eljef.me',
    description='Core functions for various utilities written by Jef Oliver',
    install_requires=['colorlog', 'PyYAML', 'xmltodict'],
    license='0BSD',
    name='eljef-core',
    packages=['eljef.core'],
    python_requires='>=3.8',
    url='https://eljef.dev/python/eljef_core',
    version='2023.11.1',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.12',
    ]
)
