# -*- coding: UTF-8 -*-
# Copyright (c) 2016, Jef Oliver
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
import logging
import os
import shutil
import tarfile

from collections import OrderedDict
from contextlib import contextmanager
from typing import AnyStr
from typing import Union
from typing import List

import xmltodict

LOGGER = logging.getLogger(__name__)


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


def delete(path: str, follow: bool=False) -> None:
    """Delete a directory, file, or link

    Deletes a directory, file, or link, ignoring errors if the target does
    not exist. If follow is provided and the path is a symlink, the parent for
    the symlink is deleted as well.

    Args:
        path: Directory, file, or link to delete
        follow: If True, and path is a symlink, the parent for the symlink is
                deleted as well.
    """
    try:
        if os.path.islink(path):
            parent = None
            if follow:
                parent = os.path.realpath(path)
            LOGGER.debug("Deleting link %s", path)
            os.unlink(path)
            if parent:
                LOGGER.debug("Deleting link target %s", parent)
                delete(parent)
        elif os.path.isdir(path):
            LOGGER.debug("Deleting directory %s", path)
            shutil.rmtree(path)
        else:
            LOGGER.debug("Deleting file %s", path)
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
        raise tarfile.TarError("File is not a compressed tar archive: %s",
                               file)
    if not os.path.isdir(path):
        raise FileNotFoundError("Specified path is not a directory: %s", path)
    LOGGER.debug("Extracting contents of %s to %s", file, path)
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
        raise tarfile.TarError("File is not a compressed tar archive: %s",
                               path)

    LOGGER.debug("Extracting file list from archive: %s", path)
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
    LOGGER.debug("Extracting file '%s' from archive '%s'", path, file_name)
    with tarfile.open(path) as tar_data:
        try:
            extracted = tar_data.extractfile(file_name)
            f_data = makestr(extracted.read()) if extracted else None
        except KeyError:
            f_data = None

    return f_data


def file_read(path: str) -> str:
    """Read file and return contents

    Reads a file into memory and returns it as a string.
    This is not a good function to use if the file is large.
    This function replaces unicode errors with "?".

    Args:
        path: Full path to the file to read.

    Returns:
        Data from file stored as a string
    """
    LOGGER.debug("Read file: %s", path)
    with open(path, errors='replace') as file_data:
        return file_data.read()


def file_write(path: str, data: AnyStr) -> None:
    """Write ``data`` to a file

    Args:
        path: Full path to the file to write `data` to.
        data: Data to write to `path`
    """
    mode = 'a' if not os.path.isfile(path) else 'w'

    LOGGER.debug("Write to file: %s", path)
    with open(path, mode) as open_file:
        total_chars = open_file.write(makestr(data))

    LOGGER.debug("Wrote %s characters", str(total_chars))


def mkdir(path: str, del_exist: bool=False) -> None:
    """Creates a directory

    Creates a directory, creating all needed subdirectories needed. If the
    directory already exists, the error is ignored. If `del_exist` is specified
    and the directory exists, it is deleted then recreated.

    Args:
        path: Path to directory to create
        del_exist: If True, and `path` already exists, delete it, then
                   recreate it.

    Raises:
        FileExistsError: If ``path`` exists but is not a directory.
    """
    create = False
    if os.path.exists(path):
        if del_exist:
            delete(path)
            create = True
        elif not os.path.isdir(path):
            raise FileExistsError("Path exists, but is not a directory: %s" %
                                  path)
    else:
        create = True

    if create:
        LOGGER.debug("Creating directory %s", path)
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
        raise FileNotFoundError("Provided path does not exist: %s" % path)
    cwd = os.getcwd()
    os.chdir(path)
    LOGGER.debug("pushd %s", path)
    yield
    os.chdir(cwd)
    LOGGER.debug("popd %s", path)


def xml_read(path: str) -> OrderedDict:
    """Reads and parses an XML file into a python dictionary.

    Args:
        path: path to XML file to read.

    Returns:
        Dictionary of parsed XML information as parsed by xmltodict

    Raises:
        FileNotFoundError: If provided path does not exist
        FileNotFoundError: If provided path exists but is not a file or a link
                           to a file.
        xml.parsers.expat.ExpatError: If the XML file is not valid XML or
                                      malformed XML.
    """
    if not os.path.exists(path):
        raise FileNotFoundError("Provided path does not exist: %s" % path)
    if not os.path.isfile(path):
        raise FileNotFoundError("Provided path exists, but is not a file: %s"
                                % path)

    f_data = file_read(path)
    LOGGER.debug("Parsing XML from: %s", path)
    return xmltodict.parse(f_data)


def xml_write(path: str, data_dict: OrderedDict, pretty: bool=True,
              full_document: bool=True, indent: str='    ') -> None:
    """Writes an OrderedDict to a file as XML data.

    Args:
        path: Path to file to write.
        data_dict: Dictionary of data to convert to XML
        pretty: If True, write the XML in pretty format with correct
                white-spacing. (Default is True)
        full_document: If True, write a full XML document, including headers.
                       (Default is True)
        indent: String to use for indenting. (Default is four spaces.)
    """
    LOGGER.debug('Converting data to string to write to file.')
    xml_string = xmltodict.unparse(data_dict, pretty=pretty,
                                   full_document=full_document, indent=indent)
    xml_string += os.linesep
    file_write(path, xml_string)
