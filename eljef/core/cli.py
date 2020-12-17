# -*- coding: UTF-8 -*-
# Copyright (c) 2017-2020, Jef Oliver
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
# cli.py : ElJef Application CLI Functions
"""ElJef Application CLI Functions

ElJef Application CLI Functions.
"""
from collections import namedtuple
from typing import List

import argparse


Arg = namedtuple('Arg', 'flags opts', defaults=[list(), dict()])
"""Arg holds information for adding a CLI argument.

Attributes:
    flags (list): List of flags to add. ie: [-f, --flag]
    opts (dict): Dictionary of keyword arguments for argparse.add_argument
"""


def args_simple(name: str, desc: str, args: List[Arg], exit_on_error: bool = True) -> argparse.Namespace:
    """Parses simple command line arguments for a program.

    Args:
        name: Program name.
        desc: Program description.
        args: List of Arg named tuples
        exit_on_error: Exit if an error is encountered

    Returns:
        And argparse namespace
    """
    parser = argparse.ArgumentParser(prog=name, description=desc, exit_on_error=exit_on_error)
    for arg in args:
        parser.add_argument(*arg.flags, **arg.opts)

    return parser.parse_args()


def print_version(name: str, version: str) -> None:
    """Prints a uniform version to the terminal, then exits.

    Technically, this should be a function in a specific CLI module. All
    ElJef programs duplicate this code, raising enough of a need to just
    create a central function.

    Args:
        name: Program name.
        version: Program version.

    Raises:
        SystemExit: Always 0
    """
    print(f"{name} - {version}")
    raise SystemExit(0)
