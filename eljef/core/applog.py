# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""ElJef Application Logging Setup."""

import logging
import sys

from colorlog import ColoredFormatter

DEFAULT_COLORS = {
    'DEBUG': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red'
}


def setup_app_logging(debug: bool, log_file: str = None, colors: dict = None) -> None:
    """Sets up the root logger.

    Args:
        debug: Enable DEBUG logging level. Default is INFO.
        log_file: If specified, logging to a file is enabled.
        colors: Colors (supported by colorlog) to enable for logging messages displayed on the console.

    Note:
        Colorized console logging is enabled by default.
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
