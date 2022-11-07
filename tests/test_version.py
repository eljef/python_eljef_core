# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""ElJef Version Test"""

import logging
import unittest

from eljef.core import __version__

logging.disable(logging.ERROR)


class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertTrue(__version__.VERSION is not None)


if __name__ == '__main__':
    unittest.main()
