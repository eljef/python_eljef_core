# -*- coding: UTF-8 -*-
# Copyright (c) 2017, Jef Oliver
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
# check.py: Version Check
"""ElJef Python Version Check.

This module holds a version check function
"""

import logging
import sys

LOGGER = logging.getLogger(__name__)


def version_check(major: int, minor: int) -> None:
    """Checks if the running version of Python is the supported version or
       newer.

    Args:
        major: Major version of Python needed.
        minor: Minor version of Python needed.

    Raises:
        Exception: If the version of Python running is not supported.
    """
    unsupported = False
    unsupported_string = 'Python version {0!s}.{1!s} or higher is required.'

    if sys.version_info[0] < major:
        unsupported = True
    if sys.version_info[0] > major and sys.version_info[1] < minor:
        unsupported = True

    if unsupported:
        LOGGER.error(unsupported_string.format(major, minor))
        raise Exception(unsupported_string.format(major, minor))
