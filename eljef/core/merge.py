# -*- coding: UTF-8 -*-
# Copyright (c) 2020-2021, Jef Oliver
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
# merge.py : Merge dictionaries with embedded dictionaries
"""ElJef Merge Dictionaries

This module holds functions to merge dictionaries that contain embedded
dictionaries.
"""

from copy import deepcopy


def merge_dictionaries(dict_a: dict, dict_b: dict) -> dict:
    """Merges two dictionaries, accounting for embedded dictionaries

    Args:
        dict_a: dictionary to be considered as original
        dict_b: dictionary of values to embed into ``dict_a``

    Returns:
        A new dictionary with values from ``dict_a`` and ``dict_b``, including embedded dicts.
    """
    new = deepcopy(dict_a)

    for key, value in dict_b.items():
        if isinstance(value, dict):
            new[key] = merge_dictionaries(new.get(key, {}), value)
        else:
            new[key] = value

    return new
