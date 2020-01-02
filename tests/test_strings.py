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
# test_strings.py : string testing operations
"""ElJef String Testing Operations

This module holds functions for testing string operations
"""

import logging
import unittest

from eljef.core import strings


logging.disable(logging.ERROR)


class TestMakeStr(unittest.TestCase):
    def test_makestr_str(self):
        self.assertEqual(strings.makestr(str("tests")), str("tests"))

    def test_makestr_utf8(self):
        self.assertEqual(strings.makestr(str("tests").encode("UTF-8")), str("tests"))


if __name__ == '__main__':
    unittest.main()
