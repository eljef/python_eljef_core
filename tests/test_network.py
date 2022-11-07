# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""ElJef Network operations testing"""

import logging
import unittest

from eljef.core import network

logging.disable(logging.ERROR)


class TestAddressIsIp(unittest.TestCase):
    def test_address_empty(self):
        self.assertEqual(network.address_is_ip(""), 0)

    def test_address_invalid(self):
        self.assertEqual(network.address_is_ip("not_an_ip"), 0)

    def test_address_is4(self):
        self.assertEqual(network.address_is_ip("192.168.1.1"), 4)

    def test_address_is6(self):
        self.assertEqual(network.address_is_ip("::ffff:c0a8:101"), 6)


if __name__ == '__main__':
    unittest.main()
