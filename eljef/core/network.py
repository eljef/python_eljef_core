# -*- coding: UTF-8 -*-
# Copyright (c) 2016-2020, Jef Oliver
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
# network.py : Network operations
"""ElJef Network operations

This module holds functionality for basic network operations
"""

import ipaddress
import logging

LOGGER = logging.getLogger(__name__)


def address_is_ip(address: str) -> int:
    """Checks if an address is an IP address.

    Args:
        address: IP address to verify.

    Returns:
        0 if address could not be verified, 4 if the address is IPv4, or 6 if the address is IPv6
    """
    LOGGER.debug("Validating IP address: %s", address)
    try:
        ret = ipaddress.ip_address(address)
    except ValueError:
        LOGGER.warning("Provided address is not a valid IP address: %s", address)
        return 0

    LOGGER.debug("Validated Address %s as IPv%d", address, ret.version)
    return ret.version
