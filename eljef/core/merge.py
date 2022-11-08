# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""Dictionary Merge Operations"""

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
