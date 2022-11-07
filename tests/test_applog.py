# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD
"""ElJef Application Logging Setup Testing"""

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


if __name__ == '__main__':
    unittest.main()
