# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

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
        TypeError: A value is a dictionary, set, or list
    """
    ret = ''
    equals_str = '=' if not kwargs.get('spaced', False) else ' = '

    for key, value in data.items():
        value_type = type(value)
        if value_type in {dict, list, set}:
            raise TypeError(f"value for key '{key}' is a {value_type}")
        ret += makestr(key) + equals_str + makestr(value) + '\n'

    return ret.strip()


def loads(data: str, **kwargs) -> dict:
    """Creates a dictionary of key value pairs from a key value pair string.

    The string is expected to contain key value pairs that are separated by new line characters,
    as if they were read from a file of the following format:
    key=value
    key2=value

    Args:
        data: Data from the read file.

    Keyword Args:
        comment: If the file contains lines with comments after data, everything after this character
                 will be stripped
    """
    ret = {}
    new_data = makestr(data.replace('\r\n', '\n')).split('\n')
    if new_data:
        for line in new_data:
            new_line = line.strip()
            if new_line and new_line[0] not in _COMMENT_CHECKS and '=' in new_line:
                inline_comment_symbol = kwargs.get('comment')
                if inline_comment_symbol:
                    line = new_line.split(inline_comment_symbol, 1)
                    key, value = line[0].split('=', 1)
                else:
                    key, value = new_line.split('=', 1)
                ret[key.strip()] = value.strip()

    return ret
