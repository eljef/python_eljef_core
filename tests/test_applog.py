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
# test_applog.py : ElJef Application Logging Setup Testing
"""ElJef Application Logging Setup Testing

ElJef Application Logging Setup Testing.
"""

import logging
import os
import tempfile
import unittest

from eljef.core import applog

logging.disable(logging.ERROR)


def _get_file() -> str:
    fd, path = tempfile.mkstemp(None, None, tempfile.gettempdir(), True)
    os.write(fd, ''.encode('UTF-8'))
    os.close(fd)

    return path


class TestSetupAppLogging(unittest.TestCase):
    def test_setup_app_logging(self):
        path = _get_file()
        applog.setup_app_logging(True, path)
