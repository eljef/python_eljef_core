# -*- coding: UTF-8 -*-
# Copyright (c) 2016-2018, Jef Oliver
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
import os

from typing import Any
from typing import Union

from eljef.core import fops
from eljef.core.check import version_check


LOGGER = logging.getLogger(__name__)

version_check(3, 6)


class Settings:
    """Builds a settings object from defaults and a provided settings file.

    Settings are loaded in hierarchy of defaults, then system-wide,
    then user-level.

    If the 'conf_back' setting is set to True in the top level of a config
    file, config files will be backed up before writing a new config file.

    Args:
        defaults: Dictionary of default values
        user_path: Full path to configuration file.
        sys_path: Full path to a system wide configuration file.

    Note:
        The settings file is expected to be stored as YAML.
        The defaults dictionary should be a complete dictionary, containing all supported settings for the program and
        their default values.
    """
    def __init__(self, defaults: dict, user_path: str = None,
                 sys_path: str = None) -> None:
        self._defaults = defaults
        self._loaded = {'system': False, 'user': False}
        self._paths = {'system': sys_path, 'user': user_path}
        self._settings = {'system': {}, 'user': {}}
        self._sets = lambda: None

        if 'conf_back' not in self._defaults:
            self._defaults['conf_back'] = False
        if sys_path:
            self._read_settings(sys_path, 'system')
        if user_path:
            self._read_settings(user_path, 'user')

        self._apply_settings()

    def _apply_setting(self, setting: str) -> None:
        if setting in self._settings['user']:
            setattr(self._sets, setting, self._settings['user'][setting])
        elif setting in self._settings['system']:
            setattr(self._sets, setting, self._settings['system'][setting])
        else:
            setattr(self._sets, setting, self._defaults[setting])

    def _apply_settings(self) -> None:
        for setting in self._defaults:
            self._apply_setting(setting)

    def _read_settings(self, path: str, settings_type: str) -> None:
        if os.path.isfile(path):
            s_data = fops.file_read_convert(path, 'yaml', True)
            self._settings[settings_type].update(s_data)
            self._loaded[settings_type] = True

    def add(self, setting: str, value: Any, sys_setting: bool = False) -> None:
        """Adds a setting

        Args:
            setting: Setting name to add
            value: Value to add to setting
            sys_setting: If True, the adds a system-wide setting rather than a user specific setting.
        """
        s_type = 'system' if sys_setting else 'user'
        self._settings[s_type][setting] = value
        self._apply_setting(setting)

    def get(self, setting: str) -> Union[Any, None]:
        """Retrieve a settings value

        Args:
            setting: Setting name that value is needed for.

        Returns:
            Value of setting or None if it doesn't exist.
        """
        return getattr(self._sets, setting, None)

    def save(self, sys_setting: bool = False, save_all: bool = False) -> None:
        """Save settings to the configuration file.

        Args:
            sys_setting: If True, a system wide configuration file will be saved rather than a user specific
                         configuration.
            save_all: If sys_setting is False, save all settings to the user file.
                      (Useful when creating a new settings file.)
        """
        s_type = 'system' if sys_setting else 'user'
        do_backup = True if self._settings[s_type].get('conf_back') else False
        sets = self._settings[s_type]
        if s_type == 'user' and save_all:
            sets = self._defaults
            sets.update(self._settings['system'])
            sets.update(self._settings['user'])
        fops.file_write_convert(self._paths[s_type], 'yaml', sets, backup=do_backup)
