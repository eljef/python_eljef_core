# -*- coding: UTF-8 -*-
# Copyright (c) 2016, Jef Oliver
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
import platform
import subprocess

LOGGER = logging.getLogger(__name__)


def address_is_ip(address: str) -> int:
    """Checks if an address is an IP address.

    Args:
        address: IP address to verify.

    Returns:
        0 if address could not be verified, 4 if the address is IPv4, or 6 if
        the address is IPv6
    """
    LOGGER.debug("Validating IP address: {0!s}".format(address))
    try:
        ret = ipaddress.ip_address(address)
    except ValueError:
        LOGGER.warning("Provided address is not a valid IP address:"
                       " {0!s}".format(address))
        return 0

    LOGGER.debug("Validated Address {0!s} as IPv{1!s}".format(address,
                                                              ret.version))
    return ret.version


def host_is_up(address: str) -> bool:
    """Sends a ping to a host to determine if it is up.

    Note:
        This will only work for hosts that do not block ICMP pings.

    Args:
        address: Address to ping

    Returns:
        True if host responded to ping, False otherwise.
    """
    p_arg = "-n" if platform.system().lower() == "windows" else "-c"
    args = ['ping', p_arg, '1', address]
    LOGGER.debug("Pinging host with: {0!s}".format(' '.join(args)))
    output = subprocess.run(args, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    return True if output.returncode == 0 else False
