# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""Basic Network Operations"""

import ipaddress
import logging

LOGGER = logging.getLogger(__name__)


def address_is_ip(address: str) -> int:
    """Checks if ``address`` is an IP address and what version it is.

    Args:
        address: IP address to verify.

    Returns:
        0 if ``address`` could not be verified, 4 if ``address`` is IPv4, or 6 if ``address`` is IPv6.
    """
    LOGGER.debug("Validating IP address: %s", address)
    try:
        ret = ipaddress.ip_address(address)
    except ValueError:
        LOGGER.warning("Provided address is not a valid IP address: %s", address)
        return 0

    LOGGER.debug("Validated Address %s as IPv%d", address, ret.version)
    return ret.version
