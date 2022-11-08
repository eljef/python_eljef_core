# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""Settings File Operations"""
import logging

from typing import Any
from typing import Union

from eljef.core import fops
from eljef.core.merge import merge_dictionaries

LOGGER = logging.getLogger(__name__)


class Settings:
    """Builds a settings object from defaults and a provided settings file.

    Settings are loaded in hierarchy of defaults, then system-wide,
    then user-level.

    Args:
        defaults: Dictionary of default values
        user_path: Full path to users YAML configuration file.
        sys_path: Full path to a system-wide YAML configuration file.

    Note:
        The settings file is expected to be stored as YAML.
        The defaults dictionary should be a complete dictionary, containing all supported settings for the program and
        their default values.
    """
    def __init__(self, defaults: dict, user_path: str = None,
                 sys_path: str = None) -> None:
        self._settings = merge_dictionaries(defaults, self.read(sys_path, user_path))

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
        ret = {}
        if system_path:
            ret = merge_dictionaries(ret, fops.file_read_convert(system_path, 'yaml', True))
        if user_path:
            ret = merge_dictionaries(ret, fops.file_read_convert(user_path, 'yaml', True))

        return ret
