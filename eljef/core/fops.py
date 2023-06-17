# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""Directory, File, and Filesystem Operations"""

from collections import OrderedDict
from contextlib import contextmanager
from pathlib import Path
from typing import AnyStr
from typing import Union

import errno
import json
import logging
import os
import shutil
import xmltodict
import yaml

from eljef.core import kv
from eljef.core.strings import makestr

LOGGER = logging.getLogger(__name__)

__CONV_DATA_TO_STR = {
    'json': json.dumps,
    'kv': kv.dumps,
    'xml': xmltodict.unparse,
    'yaml': yaml.dump
}

__CONV_DATA_TO_STR_ARGS = {
    'json': {'indent': 4},
    'kv': {'spaced': False},
    'xml': {'pretty': True, 'full_document': True, 'indent': '    '},
    'yaml': {'default_flow_style': False}
}

__CONV_STR_TO_DATA = {
    'json': json.loads,
    'kv': kv.loads,
    'xml': xmltodict.parse,
    'yaml': yaml.load
}

__CONV_STR_TO_DATA_ARGS = {
    'yaml': {'Loader': yaml.FullLoader}
}

_ERR_FILE_NOT_TAR = "File is not a compressed tar archive: {0!s}"
_ERR_PATH_NOT_DIR = "Specified path is not a directory: {0!s}"
_ERR_PATH_NOT_EXIST = "Provided path does not exist: {0!s}"
_ERR_PATH_NOT_FILE = "Provided path exists, but is not a file: {0!s}"
_ERR_DATA_TYPE = "Unsupported data_type: {0!s}"
_ERR_NO_DATA = "No data provided"

JSON = 'json'
"""JSON data type"""
KV = 'kv'
"""Key/Value data type"""
XML = 'xml'
"""XML data type"""
YAML = 'yaml'
"""YAML data type"""


def backup_path(path: str) -> None:
    """Renames a directory/file/link for backup purposes

    This will append the .bak extension to a file. If ``path``.bak exists, a number is appended until a non-existent
    file is found.
    ie: file.bak file.bak.1 file.bak.2

    Args:
        path: Full path to item to back up
    """
    base_back = f"{path}.bak"
    new_path = base_back
    num_backups = 0

    if os.path.exists(path):
        if os.path.exists(new_path):
            while os.path.exists(new_path):
                num_backups += 1
                new_path = f"{base_back}.{num_backups}"
        LOGGER.debug("Backing up file: %s -> %s", path, new_path)
        os.rename(path, new_path)


def delete(path: str, follow: bool = False, backup: bool = False) -> None:
    """Delete a directory, file, or link

    Deletes a directory, file, or link, ignoring errors if the target does
    not exist. If follow is provided and the path is a symlink, the parent for
    the symlink is deleted as well.

    Args:
        path: Directory, file, or link to delete
        follow: If True, and ``path`` is a symlink, the parent for the symlink is deleted as well.
        backup: If True, backup ``path`` before deleting.

    Note:
        If ``path`` is a symlink and ``follow`` is not True, the link will still be unlinked, and the parent will be
        retained instead of being deleted. The parent will need to be backed up or deleted separately.
    """
    try:
        if os.path.islink(path):
            parent = None
            if follow:
                parent = os.path.realpath(path)
            LOGGER.debug("Deleting link %s", path)
            os.unlink(path)
            if parent and not backup:
                LOGGER.debug("Deleting link target %s", parent)
                delete(parent)
        else:
            if backup:
                backup_path(path)
                return
            if os.path.isdir(path):
                LOGGER.debug("Deleting directory %s", path)
                shutil.rmtree(path)
            else:
                LOGGER.debug("Deleting file %s", path)
                os.remove(path)
    except (IOError, OSError) as err:
        if err.errno != errno.ENOENT:
            raise


def file_read(path: str, strip: bool = False) -> str:
    """Read file and return contents

    Reads a file into memory and returns it as a string.
    This is not a good function to use if the file is large.

    Args:
        path: Full path to the file to read.
        strip: If True, the returned string will have the .strip() function called on it.

    Returns:
        Data from file stored as a string

    Note:
        This function replaces unicode errors with "?".
    """
    LOGGER.debug("Read file: %s", path)
    with open(path, errors='replace', encoding='utf8') as file_data:
        return file_data.read().strip() if strip else file_data.read()


def file_read_convert(path: str, data_type: str, default: bool = False) -> Union[dict, OrderedDict]:
    """Reads and parses a file into a python dictionary using the specified ``data_type`` module.

    Args:
        path: Path to file to read.
        data_type: Type of data contained. (JSON, KV, XML, YAML)
        default: If true and the file is missing, an empty dictionary will be returned.

    Returns:
        A dictionary of parsed data.

    Raises:
        FileNotFoundError: If provided ``path`` does not exist and ``default`` is not True.
        IOError: If provided ``path`` exists but is not a file or a link to a file.
        ValueError: Unsupported ``data_type``
    """
    data_type_lower = data_type.lower()

    if data_type_lower not in __CONV_STR_TO_DATA:
        raise ValueError(_ERR_DATA_TYPE.format(data_type))

    if not os.path.exists(path):
        if not default:
            raise FileNotFoundError(_ERR_PATH_NOT_EXIST.format(path))
        return {}

    if not os.path.isfile(path):
        raise IOError(_ERR_PATH_NOT_FILE.format(path))

    f_data = file_read(path)
    LOGGER.debug("Parsing %s from: %s", data_type.upper, path)

    if data_type_lower in __CONV_STR_TO_DATA_ARGS:
        return __CONV_STR_TO_DATA[data_type_lower](f_data, **__CONV_STR_TO_DATA_ARGS[data_type_lower])

    return __CONV_STR_TO_DATA[data_type_lower](f_data)


def file_write(path: str, data: AnyStr, backup: bool = False, newline: str = None) -> None:
    """Write ``data`` to a file

    Args:
        path: Full path to the file to write `data` to.
        data: Data to write to ``path``
        backup: Backup the file before writing to it. (Default is False.)
        newline: Passed to the open function for newline translation. The default
            of None lets native translation happen.
    """
    mode = 'a' if not os.path.isfile(path) else 'w'

    if backup:
        backup_path(path)

    LOGGER.debug("Write to file: %s", path)
    with open(path, mode, newline=newline, encoding='utf8') as open_file:
        total_chars = open_file.write(makestr(data))
        LOGGER.debug("Wrote %d characters", total_chars)


def file_write_convert_defaults(data_type: str) -> dict:
    """Returns a dictionary of defaults to be used with :func:`file_write_convert`

    Args:
        data_type: Type of data contained. (JSON, KV, XML, YAML)

    Returns:
        A dictionary of keyword arguments to be passed to :func:`file_write_convert`

    Raises:
        ValueError: Unsupported ``data_type``

    Note:
        The returned dictionary contains defaults that :func:`file_write_convert` uses for writing different files.
        These defaults can be changed. Extra options can be appended to the dictionary as well. You'll need to read
        each dumpers documentation for argument information.

        Dumper Defaults:
            JSON -> json.dumps:
                indent: 4
            KV -> kv.dumps:
                spaced: False
            XML -> xmltodict.unparse:
                pretty: True
                full_document: True,
                indent: '    '
            YAML -> yaml.dump (PyYAML):
                default_flow_style: False
    """
    if data_type.lower() not in __CONV_DATA_TO_STR_ARGS:
        raise ValueError(_ERR_DATA_TYPE.format(data_type))
    return __CONV_DATA_TO_STR_ARGS[data_type.lower()]


def file_write_convert(path: str, data_type: str, data: Union[dict, OrderedDict], **kwargs) -> None:
    """Writes a Python dictionary to file using the specified ``data_type`` module for conversion.

    Args:
        path: Full path to the file to write ``data`` to.
        data_type: Type of data contained. (JSON, KV, XML, YAML)
        data: Data to write to ``path``.

    Keyword Args:
        backup: Backup ``path`` before writing to it. (Default is False.)
        dumper_args: A dictionary of keyword arguments to pass to the specified dumper.
                     See :func:`file_write_convert_defaults`
    """
    dumper_kwargs = file_write_convert_defaults(data_type)
    dumper_args = kwargs.get('dumper_args', None)
    if dumper_args:
        dumper_kwargs.update(dumper_args)

    LOGGER.debug('Converting data to string to write to file.')
    dumper = __CONV_DATA_TO_STR[data_type.lower()]
    write_string = dumper(data, **dumper_kwargs).replace('\r\n', '\n') + '\n'
    file_write(path, write_string, backup=kwargs.get('backup', False), newline='\n')


def list_dirs_by_extension(base_path: str, file_ext: str) -> set:
    """Creates a list of directories containing files of ``file_ext``.

    Args:
        base_path: Full path to the base directory to traverse for files.
        file_ext: Extension for files to find. This should not contain wild cards.

    Returns:
        A set of directories that contain files with ``file_ext``, relative to
        ``base_path``.

    Note:
        Returned paths are relative to ``base_path``.
    """
    dirs = []
    with pushd(base_path):
        for path in Path().rglob(f'*.{file_ext}'):
            dirs.append(os.path.join(*path.parent.parts))

    return set(dirs)


def list_files_by_extension(base_path: str, file_ext: str) -> list:
    """Creates a list of files by ``file_ext``, relative to the provided ``base_path``.

    Args:
        base_path: Full path to the base directory to traverse for files.
        file_ext: Extension for files to find. This should not contain wild cards or dots.

    Returns:
        A list of files by ``file_ext``, relative to the provided ``base_path``.

    Note:
        If no files of the type ``file_ext`` are found, an empty list is returned.
    """
    files = []
    with pushd(base_path):
        for path in Path().rglob(f'*.{file_ext}'):
            files.append(os.path.join(*path.parts))

    return files


@contextmanager
def pushd(path: str) -> None:
    """Pythonic implementation of pushd/popd

    Args:
        path: Directory to switch to.

    Raises:
        FileNotFoundError: If provided path does not exist

    Example:
        >>> with pushd('/path/to/dir'):
        >>>     print('moved to new directory')
        >>>     print(os.getcwd())
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(_ERR_PATH_NOT_EXIST.format(path))
    cwd = os.getcwd()
    os.chdir(path)
    LOGGER.debug("pushd %s", path)
    yield
    os.chdir(cwd)
    LOGGER.debug("popd %s", path)


def required_executables(executables: list) -> None:
    """Checks if the list of required executables are available.

    Args:
        executables: List of executables required to run the calling program.

    Raises:
        SystemExit: When an executable is not found.
    """
    for executable in executables:
        if not shutil.which(executable):
            raise SystemExit(f"Required executable not found: {executable}")
