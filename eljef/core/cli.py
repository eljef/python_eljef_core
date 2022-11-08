# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""CLI Application Functionality"""

from collections import namedtuple
from typing import List

import argparse


Arg = namedtuple('Arg', 'flags opts', defaults=[[], {}])
"""Arg holds information needed to add a CLI argument.

Attributes:
    flags (list): List of flags to add. ie: [-f, --flag]
    opts (dict): Dictionary of keyword arguments for argparse.add_argument
"""


def args_simple(name: str, desc: str, args: List[Arg], exit_on_error: bool = True) -> argparse.Namespace:
    """Parses simple command line arguments for a program.

    Args:
        name: Program name.
        desc: Program description.
        args: List of :class:`Arg`
        exit_on_error: Exit if an error is encountered

    Returns:
        argparse.Namespace
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
