# -*- coding: UTF-8 -*-
# Copyright (c) 2016, Jef Oliver
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU Lesser General Public License,
# version 2.1, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
# more details.
#
# Authors:
# Jef Oliver <jef@eljef.me>
#
# hash.py : Functions for encoding and hashing data
"""ElJef Data Encoding and Hashing

This module holds functions for encoding and hashing data.
"""

import base64
import hashlib
import logging
import os

from eljef.core import fops

LOGGER = logging.getLogger(__name__)
BLOCK_SIZE = 65536


def encode_base64(path: str) -> str:
    """Reads a file and converts the data to a base64 encode string

    Args:
        path: File to base64 encode contents of

    Raises:
        FileNotFoundError: When file does not exist
        IOError: When specified path is not a file

    Returns:
        Base64 encoded data as a string
    """
    if not os.path.exists(path):
        raise FileNotFoundError("Specified file does not exist: %s" % path)
    if not os.path.isfile(path):
        raise IOError("Specified path is not a file: %s" % path)
    with open(path, 'rb') as file_data:
        return fops.makestr(base64.b64encode(file_data.read()))


def hash_md5(path: str) -> str:
    """Creates a MD5 hash for ``path``

    Args:
        path: Full path to file to create hash for.

    Returns:
        string form of MD5 hash

    Raises:
        FileNotFoundError: When file does not exist
        IOError: When specified path is not a file
    """
    if not os.path.exists(path):
        raise FileNotFoundError("Specified file does not exist: %s" % path)
    if not os.path.isfile(path):
        raise IOError("Specified path is not a file: %s" % path)

    LOGGER.debug("Generating MD5 hash for %s", path)
    h_md5 = hashlib.md5()
    with open(path, 'rb') as hash_file:
        buf = hash_file.read(BLOCK_SIZE)
        while len(buf) > 0:
            h_md5.update(buf)
            buf = hash_file.read(BLOCK_SIZE)

    return fops.makestr(h_md5.hexdigest())


def hash_sha256(path: str) -> str:
    """Creates a SHA256 hash for `path`

    Args:
        path: Full path to file to create hash for.

    Returns:
        string form of SHA256 hash

    Raises:
        FileNotFoundError: When file does not exist
        IOError: When specified path is not a file
    """
    if not os.path.exists(path):
        raise FileNotFoundError("Specified file does not exist: %s" % path)
    if not os.path.isfile(path):
        raise IOError("Specified path is not a file: %s" % path)

    LOGGER.debug("Generating SHA256 hash for %s", path)
    h_sha256 = hashlib.sha256()
    with open(path, 'rb') as hash_file:
        buf = hash_file.read(BLOCK_SIZE)
        while len(buf) > 0:
            h_sha256.update(buf)
            buf = hash_file.read(BLOCK_SIZE)

    return fops.makestr(h_sha256.hexdigest())
