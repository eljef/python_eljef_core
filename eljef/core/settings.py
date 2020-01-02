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
# settings.py : Functions for handling settings
"""ElJef Settings Handling

This module holds functionality for handling of a programs stored settings.
"""
import logging

from typing import Any
from typing import Union

from eljef.core import fops

LOGGER = logging.getLogger(__name__)


class Settings:
    """Builds a settings object from defaults and a provided settings file.

    Settings are loaded in hierarchy of defaults, then system-wide,
    then user-level.

    Args:
        defaults: Dictionary of default values
        user_path: Full path to users YAML configuration file.
        sys_path: Full path to a system wide YAML configuration file.

    Note:
        The settings file is expected to be stored as YAML.
        The defaults dictionary should be a complete dictionary, containing all supported settings for the program and
        their default values.
    """
    def __init__(self, defaults: dict, user_path: str = None,
                 sys_path: str = None) -> None:
        self._settings = defaults
        self._settings.update(self.read(sys_path, user_path))

    def get(self, setting: str) -> Union[Any, None]:
        """Retrieve a settings value

        Args:
            setting: Setting name that value is needed for.

        Returns:
            Value of setting or None if it doesn't exist.
        """
        return self._settings.get(setting)

    def get_all(self) -> dict:
        """Returns all stored settings

        Returns;
            A dictionary with all settings
        """
        return self._settings

    @staticmethod
    def read(system_path: str, user_path: str) -> dict:
        """Reads specified yaml configuration files

        Args:
            system_path: Full path to system wide YAML config file
            user_path: Full path to users YAML config file

        Returns:
            A dictionary filled with system settings, overlapped with the user specific settings
        """
        settings_data = fops.file_read_convert(system_path, 'yaml', True)
        settings_data.update(fops.file_read_convert(user_path, 'yaml', True))

        return settings_data
