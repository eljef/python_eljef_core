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
# check.py: Version Check
"""ElJef Python Version Check.

This module holds a version check function
"""

import logging
import sys

LOGGER = logging.getLogger(__name__)

_STR_UNSUPPORTED = 'Python version {0!s}.{1!s} or higher is required.'


class VersionError(Exception):
    """Custom Exception for Version Checking.

    Args:
        major: Major version of Python required
        minor: Minor version of Python required
    """
    def __init__(self, major: int, minor: int) -> None:
        message = _STR_UNSUPPORTED.format(major, minor)
        super(VersionError, self).__init__(message)
        self.message = message
        self.major = major
        self.minor = minor


def version_check(major: int, minor: int) -> None:
    """Checks if the running version of Python is the supported version or newer.

    Args:
        major: Major version of Python needed.
        minor: Minor version of Python needed.

    Raises:
        Exception: If the version of Python running is not supported.
    """
    if sys.version_info[0] < major:
        raise VersionError(major, minor)
    if sys.version_info[0] >= major and sys.version_info[1] < minor:
        raise VersionError(major, minor)
