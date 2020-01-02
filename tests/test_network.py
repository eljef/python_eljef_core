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
# test_network.py : Network testing operations
"""ElJef Network operations testing

This module holds functionality for testing basic network operations
"""

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


class TestHostIsUp(unittest.TestCase):
    def test_host_is_up_down(self):
        self.assertFalse(network.host_is_up("0.1.2.3"))  # hopefully this address doesn't exist on the machine

    def test_host_is_up_up(self):
        # this will need to be changed to something reachable on networks that are proxied or filtered
        self.assertTrue(network.host_is_up("1.1.1.1"))


if __name__ == '__main__':
    unittest.main()
