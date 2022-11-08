# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""String Operations"""

from typing import AnyStr


def makestr(data: AnyStr) -> str:
    """Return a decoded string

    If ``data`` is encoded (bytes), it is decoded before returned.

    Args:
        data: data to return decoded

    Returns:
        Decoded string
    """
    try:
        return str(data.decode('utf-8'))
    except AttributeError:
        return str(data)
