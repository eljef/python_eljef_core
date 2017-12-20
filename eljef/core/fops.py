# -*- coding: UTF-8 -*-
# Copyright (c) 2016-2017, Jef Oliver
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
# fops.py : Directory, File, and Filesystem operations
"""ElJef Directory, File, and Filesystem operations.

This module holds functions for performing operations on directories, files,
and filesystems (permissions for directories and files).
"""

import errno
import json
import logging
import os
import shutil
import tarfile
import xmltodict
import yaml

from collections import OrderedDict
from contextlib import contextmanager
from typing import AnyStr
from typing import Union
from typing import List

from eljef.core.check import version_check

LOGGER = logging.getLogger(__name__)

version_check(3, 6)

__CONV_DATA_TO_STR = {
    'json': json.dumps,
    'xml': xmltodict.unparse,
    'yaml': yaml.dump
}

__CONV_DATA_TO_STR_ARGS = {
    'json': {'indent': 4},
    'xml': {'pretty': True, 'full_document': True, 'indent': '    '},
    'yaml': {'default_flow_style': False}
}

__CONV_STR_TO_DATA = {
    'json': json.loads,
    'xml': xmltodict.parse,
    'yaml': yaml.load
}


def makestr(data: AnyStr) -> str:
    """Return a decoded string

    If ``data`` is encoded (bytes), it is decoded before returned.

    Args:
        data: data to return decoded

    Returns:
        Decoded string
    """
    try:
        return str(data.decode('utf-8'))
    except AttributeError:
        return str(data)


def backup_path(path: str) -> None:
    """Renames a directory/file/link for backup purposes

    This will append the .bak extension to a file. If path.bak exists, a number
    is appended until a non-existent file is found.
    ie: file.bak file.bak.1 file.bak.2

    Args:
        path: Full path to item to backup
    """
    base_back = "{0!s}.bak".format(path)
    new_path = base_back
    num_backups = 0

    if os.path.exists(path):
        if os.path.exists(new_path):
            while os.path.exists(new_path):
                num_backups += 1
                new_path = "{0!s}.{1!s}".format(base_back, num_backups)
        LOGGER.debug("Backing up file: {0!s} -> {1!s}".format(path, new_path))
        os.rename(path, new_path)


def delete(path: str, follow: bool=False, backup: bool=False) -> None:
    """Delete a directory, file, or link

    Deletes a directory, file, or link, ignoring errors if the target does
    not exist. If follow is provided and the path is a symlink, the parent for
    the symlink is deleted as well.

    Args:
        path: Directory, file, or link to delete
        follow: If True, and path is a symlink, the parent for the symlink is
                deleted as well.
        backup: If True, backup `path` before deleting. (If `path` is a
                symlink, the link will still be unlinked, and the parent will
                be retained instead of being deleted. The parent will need to
                be backed up or deleted separately.)
    """
    try:
        if os.path.islink(path):
            parent = None
            if follow:
                parent = os.path.realpath(path)
            LOGGER.debug("Deleting link {0!s}".format(path))
            os.unlink(path)
            if parent and not backup:
                LOGGER.debug("Deleting link target {0!s}".format(parent))
                delete(parent)
        else:
            if backup:
                backup_path(path)
            if os.path.isdir(path):
                LOGGER.debug("Deleting directory {0!s}".format(path))
                shutil.rmtree(path)
            else:
                LOGGER.debug("Deleting file {0!s}".format(path))
                os.remove(path)
    except (IOError, OSError) as err:
        if err.errno != errno.ENOENT:
            raise


def extract(file: str, path: str) -> None:
    """Extracts contents of a compressed file to path

    Args:
        file: File to extract contents of
        path: Path to directory to extract contents of compressed file to

    Raises:
        FileNotFoundError: If specified path is not a directory
        tarfile.Tarfile: If specified file is not a compressed tar archive
    """
    if not tarfile.is_tarfile(file):
        raise tarfile.TarError("File is not a compressed tar archive:"
                               " {0!s}".format(file))
    if not os.path.isdir(path):
        raise FileNotFoundError("Specified path is not a directory:"
                                " {0!s}".format(path))
    LOGGER.debug("Extracting contents of {0!s} to {1!s}".format(file, path))
    with tarfile.open(file) as file_data:
        file_data.extractall(path=path)


def extract_file_list(path: str, ignore_dots: bool=False) -> List[str]:
    """Extracts a file list from the provided archive

    Args:
        path: Full path to tar archive to extract file list from.
        ignore_dots: If True, files with a leading dot are ignored. (Hidden
                     files.)

    Returns:
        List of files in archive

    Raises:
        tarfile.Tarfile: If specified file is not a compressed tar archive
    """
    if not tarfile.is_tarfile(path):
        raise tarfile.TarError("File is not a compressed tar archive:"
                               " {0!s}".format(path))

    LOGGER.debug("Extracting file list from archive:"
                 " {0!s}".format(path))
    with tarfile.open(path) as tar_data:
        file_list = tar_data.getnames()

    if ignore_dots:
        for name in file_list:
            if os.path.basename(name).startswith('.'):
                file_list.remove(name)

    return file_list


def file_extract(path: str, file_name: str) -> Union[str, None]:
    """Extracts file and return contents

    Extracts ``file_name`` from ``file`` and returns it as a string.

    Args:
        path: Full path to the archive to extract `file_name` from
        file_name: Name of file to extract from `path`

    Returns:
        Data from ``file_name`` stored as a string or None if not found
    """
    LOGGER.debug("Extracting file '{0!s}' from archive"
                 " '{1!s}'".format(path, file_name))
    with tarfile.open(path) as tar_data:
        try:
            extracted = tar_data.extractfile(file_name)
            f_data = makestr(extracted.read()) if extracted else None
        except KeyError:
            f_data = None

    return f_data


def file_read(path: str, strip: bool=False) -> str:
    """Read file and return contents

    Reads a file into memory and returns it as a string.
    This is not a good function to use if the file is large.
    This function replaces unicode errors with "?".

    Args:
        path: Full path to the file to read.
        strip: If True, the returned string will have the .strip() function
               called on it.

    Returns:
        Data from file stored as a string
    """
    LOGGER.debug("Read file: {0!s}".format(path))
    with open(path, errors='replace') as file_data:
        return file_data.read().strip() if strip else file_data.read()


def file_read_convert(path: str, data_type: str,
                      default: bool=False) -> Union[dict, OrderedDict]:
    """Reads and parses a file into a python dictionary using the specified
       ``data_type`` module.

    Args:
        path: Path to file to read.
        data_type: Type of data contained.
                   Supported: JSON, XML, YAML
        default: If true and the file is missing, an empty dictionary will be
                 returned.

    Returns:
        A dictionary of parsed data.

    Raises:
        FileNotFoundError: If provided path does not exist and
                           ``default`` is not True.
        FileNotFoundError: If provided path exists but is not a file or a link
                           to a file.
        ValueError: Unsupported ``data_type``
    """
    if data_type.lower() not in __CONV_STR_TO_DATA:
        raise ValueError("Unsupported data_type: {0!s}".format(data_type))

    if not os.path.exists(path):
        if default:
            return dict()
        else:
            raise FileNotFoundError("Provided path does not exist:"
                                    " {0!s}".format(path))
    if not os.path.isfile(path):
        raise FileNotFoundError("Provided path exists, but is not a file:"
                                " {0!s}".format(path))

    f_data = file_read(path)
    LOGGER.debug("Parsing {0!s} from: {1!s}".format(data_type.upper, path))
    return __CONV_STR_TO_DATA[data_type.lower()](f_data)


def file_write(path: str, data: AnyStr, backup: bool=False,
               newline: str=None) -> None:
    """Write ``data`` to a file

    Args:
        path: Full path to the file to write `data` to.
        data: Data to write to `path`
        backup: Backup the file before writing to it. (Default is False.)
        newline: Passed to the open function for newline translation. The
                 default of None lets native translation happen.
    """
    mode = 'a' if not os.path.isfile(path) else 'w'

    if backup:
        backup_path(path)

    LOGGER.debug("Write to file: {0!s}".format(path))
    with open(path, mode, newline=newline) as open_file:
        total_chars = open_file.write(makestr(data))
        LOGGER.debug("Wrote {0!s} characters".format(total_chars))


def file_write_convert_defaults(data_type: str) -> dict:
    """Returns a dictionary of defaults to be used with file_write_convert

    Args:
        data_type: Type of data contained.
                   Supported: JSON, XML, YAML

    Returns:
        A dictionary of keyword arguments to be passed to file_write_convert

    Raises:
        ValueError: Unsupported ``data_type``

    Note:
        The returned dictionary contains defaults that eljef.core.fops uses
        for writing different files. These defaults can be changed. Extra
        options can be appended to the dictionary as well. You'll need to read
        each dumpers documentation for argument information.

        Dumper Defaults:
            JSON -> json.dumps:
                indent: 4
            XML -> xmltodict.unparse:
                pretty: True
                full_document: True,
                indent: '    '
            YAML -> yaml.dump (PyYAML):
                default_flow_style: False
    """
    if data_type.lower() not in __CONV_DATA_TO_STR_ARGS:
        raise ValueError("Unsupported data_type: {0!s}".format(data_type))
    return __CONV_DATA_TO_STR_ARGS[data_type.lower()]


def file_write_convert(path: str, data_type: str,
                       data: Union[dict, OrderedDict],
                       backup: bool=False, dumper_args: dict=None) -> None:
    """Writes a Python dictionary to file using the specified ``data_type``
       module for conversion.

    Args:
        path: Full path to the file to write `data` to.
        data_type: Type of data contained.
                   Supported: JSON, XML, YAML
        data: Data to write to `path`
        backup: Backup the file before writing to it. (Default is False.)
        dumper_args: A dictionary of keyword arguments to pass to the
                     specified dumper. See ``file_write_convert_defaults``
    """
    dumper_kwargs = file_write_convert_defaults(data_type)
    if dumper_args:
        dumper_kwargs.update(dumper_args)

    LOGGER.debug('Converting data to string to write to file.')
    dumper = __CONV_DATA_TO_STR[data_type.lower()]
    write_string = dumper(data, **dumper_kwargs).replace('\r\n', '\n') + '\n'
    file_write(path, write_string, backup=backup, newline='\n')


def mkdir(path: str, del_exist: bool=False, backup: bool=False) -> None:
    """Creates a directory

    Creates a directory, creating all needed subdirectories needed. If the
    directory already exists, the error is ignored. If `del_exist` is specified
    and the directory exists, it is deleted then recreated.

    Args:
        path: Path to directory to create
        del_exist: If True, and `path` already exists, delete it, then
                   recreate it.
        backup: If True and `del_exist` is True, backup the existing directory
                before deleting it.

    Raises:
        FileExistsError: If ``path`` exists but is not a directory.
    """
    create = False
    if os.path.exists(path):
        if del_exist:
            delete(path, backup=backup)
            create = True
        elif not os.path.isdir(path):
            raise FileExistsError("Path exists, but is not a directory:"
                                  " {0!s}".format(path))
    else:
        create = True

    if create:
        LOGGER.debug("Creating directory {0!s}".format(path))
        os.makedirs(path)


@contextmanager
def pushd(path: str) -> None:
    """Pythonic implementation of pushd/popd

    Args:
        path: Directory to switch to.

    Raises:
        FileNotFoundError: If provided path does not exist

    Examples:
    >>> with pushd('/path/to/dir'):
    >>>     print('moved to new directory')
    >>>     print(os.getcwd())
    """
    if not os.path.isdir(path):
        raise FileNotFoundError("Provided path does not exist:"
                                " {0!s}".format(path))
    cwd = os.getcwd()
    os.chdir(path)
    LOGGER.debug("pushd {0!s}".format(path))
    yield
    os.chdir(cwd)
    LOGGER.debug("popd {0!s}".format(path))
