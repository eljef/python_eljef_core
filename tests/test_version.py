# -*- coding: UTF-8 -*-
# Copyright (c) 2020, Jef Oliver
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
# test_version.py : ElJef Version Test
"""ElJef Version Test

ElJef Version Test
"""

import logging
import unittest

from eljef.core import __version__

logging.disable(logging.ERROR)


class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertTrue(__version__.VERSION is not None)
