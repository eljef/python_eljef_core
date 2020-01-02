# -*- coding: UTF-8 -*-
# Copyright (c) 2017-2020, Jef Oliver
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
# dictobj.py : Dictionary Object
"""ElJef Dictionary Object

This module holds the Dictionary Object class.
"""

import logging

from collections import abc
from typing import Any, Mapping

LOGGER = logging.getLogger(__name__)


class DictObj(abc.Mapping):
    """Builds an object from a dictionary

    Recurses a dictionary, converting it to an object, while maintaining compatibility with dictionary
    methods. This can be used as a dictionary, or as an object with the dictionary keys as object attributes.

    Args:
        dictionary: Dictionary to convert to DictObj.

    Raises:
        AttributeError: If a key or attribute is missing.
        TypeError: If supplied dictionary is not a dict.

    Examples:
        >>> t = {'key': 'value'}
        >>> u = DictObj(t)
        >>> u['key']
            'value'
        >>> u.key
            'value'

    """
    def __init__(self, dictionary: dict = None) -> None:
        if dictionary:
            for key, value in dictionary.items():
                if not hasattr(self, key):
                    if isinstance(value, dict):
                        self.__dict__[key] = DictObj(value)
                    else:
                        self.__dict__[key] = value

    def __contains__(self, item: Any) -> bool:
        return self.__dict__.__contains__(item)

    def __iter__(self) -> Any:
        return self.__dict__.__iter__()

    def __delattr__(self, item: str) -> None:
        try:
            self.__dict__.__delitem__(item)
        except KeyError:
            raise AttributeError("'{0} object has no attribute '{1}'".format(self.__class__.__name__, item))

    def __getattr__(self, item: str) -> Any:
        try:
            return self.__dict__[item]
        except KeyError:
            raise AttributeError("'{0} object has no attribute '{1}'".format(self.__class__.__name__, item))

    def __delitem__(self, item: Any) -> None:
        self.__dict__.__delitem__(item)

    def __getitem__(self, value: Any) -> Any:
        return self.__dict__[value]

    def __len__(self) -> int:
        return self.__dict__.__len__()

    def __repr__(self) -> str:
        return '{%s}' % str(', '.join('%s : %s' % (key, repr(value)) for (key, value) in self.__dict__.items()))

    def __setattr__(self, key: Any, value: Any) -> None:
        self.__dict__[key] = value

    def __setitem__(self, key: Any, value: Any) -> None:
        self.__dict__[key] = value

    def to_dict(self) -> dict:
        """Dumps a dictionary form of the DictObj object.

        Returns:
            A dictionary form of the DictObj object.
        """
        ret = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, DictObj):
                ret[key] = self.__dict__[key].to_dict()
            else:
                ret[key] = self.__dict__[key]

        return ret

    def update(self, new_dict: Mapping, **kwargs) -> None:
        """Update updates the DictObj with the provided dictionary or iterable

        Args:
            new_dict: dictionary or iterable to update dictionary from

        Note:
            Keyword args are iterated and used to update the DictObj
        """
        self.__dict__.update(new_dict, **kwargs)
