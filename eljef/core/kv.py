# -*- coding: UTF-8 -*-
# Copyright (c) 2017-2018, Jef Oliver
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
# kv.py : Key/Value Reading/Writing
"""ElJef Key/Value Reading/Writing

This module holds functions to read and write key/value pairs to and from single strings
ie: data from files
"""

from eljef.core.strings import makestr

_COMMENT_CHECKS = [';', '#', '/']


def dumps(data: dict, **kwargs) -> str:
    """Dumps a dictionary to a key/value pair string for writing to a file.

    Args:
        data: dictionary to convert to key/value pair string

    Keyword Args:
        spaced: Add a space around the equals sign separating the key and value

    Raises:
        TypeError if a value is a dictionary, set, or list
    """
    ret = ''
    equals_str = '=' if not kwargs.get('spaced', False) else ' = '

    for key, value in data.items():
        value_type = type(value)
        if value_type in {dict, list, set}:
            raise TypeError("value for key '{0}' is a {1}".format(key, value_type))
        ret += makestr(key) + equals_str + makestr(value) + '\n'

    return ret.strip()


def loads(data: str) -> dict:
    """Creates a dictionary of key value pairs from a key value pair string.

    The string is expected to contain key value pairs that are separated by new line characters,
    as if they were read from a file of the following format:
    key=value
    key2=value

    Args:
        data: Data from the read file.
    """
    ret = dict()
    new_data = makestr(data.replace('\r\n', '\n')).split('\n')
    if new_data:
        for line in new_data:
            new_line = line.strip()
            if new_line and new_line[0] not in _COMMENT_CHECKS and '=' in new_line:
                key, value = new_line.split('=', 1)
                ret[key.strip()] = value.strip()

    return ret
