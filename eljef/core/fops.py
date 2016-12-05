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

import base64
import errno
import hashlib
import logging
import os
import shutil
import tarfile

from contextlib import contextmanager
from typing import AnyStr
from typing import Union
from typing import List

LOGGER = logging.getLogger(__name__)
BLOCK_SIZE = 65536


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


def encode_base64(path: str) -> str:
    """Reads a file and converts the data to a base64 encode string

    Args:
        path: File to base64 encode contents of

    Raises:
        FileNotFoundError: When file does not exist
        IOError: When specified path is not a file

    Returns:
        Base64 encoded data as a string
    """
    if not os.path.exists(path):
        raise FileNotFoundError("Specified file does not exist: %s" % path)
    if not os.path.isfile(path):
        raise IOError("Specified path is not a file: %s" % path)
    with open(path, 'rb') as file_data:
        return makestr(base64.b64encode(file_data.read()))


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


def hash_md5(path: str) -> str:
    """Creates a MD5 hash for ``path``

    Args:
        path: Full path to file to create hash for.

    Returns:
        string form of MD5 hash

    Raises:
        FileNotFoundError: When file does not exist
        IOError: When specified path is not a file
    """
    if not os.path.exists(path):
        raise FileNotFoundError("Specified file does not exist: %s" % path)
    if not os.path.isfile(path):
        raise IOError("Specified path is not a file: %s" % path)

    LOGGER.debug("Generating MD5 hash for %s", path)
    h_md5 = hashlib.md5()
    with open(path, 'rb') as hash_file:
        buf = hash_file.read(BLOCK_SIZE)
        while len(buf) > 0:
            h_md5.update(buf)
            buf = hash_file.read(BLOCK_SIZE)

    return makestr(h_md5.hexdigest())


def hash_sha256(path: str) -> str:
    """Creates a SHA256 hash for `path`

    Args:
        path: Full path to file to create hash for.

    Returns:
        string form of SHA256 hash

    Raises:
        FileNotFoundError: When file does not exist
        IOError: When specified path is not a file
    """
    if not os.path.exists(path):
        raise FileNotFoundError("Specified file does not exist: %s" % path)
    if not os.path.isfile(path):
        raise IOError("Specified path is not a file: %s" % path)

    LOGGER.debug("Generating SHA256 hash for %s", path)
    h_sha256 = hashlib.sha256()
    with open(path, 'rb') as hash_file:
        buf = hash_file.read(BLOCK_SIZE)
        while len(buf) > 0:
            h_sha256.update(buf)
            buf = hash_file.read(BLOCK_SIZE)

    return makestr(h_sha256.hexdigest())


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
