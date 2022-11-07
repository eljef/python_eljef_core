# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""ElJef String Testing Operations"""

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
