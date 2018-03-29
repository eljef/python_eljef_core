# -*- coding: UTF-8 -*-
# Copyright (c) 2017, Jef Oliver
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
# applog.py : ElJef Application Logging Setup
"""ElJef Application Logging Setup

ElJef Application Logging Setup.
"""
import logging
import sys

from colorlog import ColoredFormatter

from eljef.core.check import version_check

version_check(3, 6)

DEFAULT_COLORS = {
    'DEBUG': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red'
}


def setup_app_logging(debug: bool, log_file: str = None,
                      colors: dict = None) -> None:
    """Sets up the root logger. Colorized console logging is enabled by default.

    Args:
        debug: Enable DEBUG logging level. Default is INFO.
        log_file: If specified, logging to a file is enabled.
        colors: Colors (supported by colorlog) to enable for logging messages displayed on the console.
    """
    color_dict = colors if colors else DEFAULT_COLORS

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    c_formatter = ColoredFormatter('%(log_color)s%(message)s', log_colors=color_dict)
    c_handler = logging.StreamHandler(sys.stdout)
    c_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    c_handler.setFormatter(c_formatter)
    logger.addHandler(c_handler)

    if log_file:
        l_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        f_formatter = logging.Formatter(l_format)
        f_handler = logging.FileHandler(log_file)
        f_handler.setLevel(logging.DEBUG)
        f_handler.setFormatter(f_formatter)
        logger.addHandler(f_handler)
