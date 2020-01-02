# -*- coding: UTF-8 -*-
# Copyright (c) 2020, Jef Oliver
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
# test_fops.py : Directory, File, and Filesystem operations Testing
"""ElJef Directory, File, and Filesystem operations testing.

This module holds functions for testing performing operations on directories, files, and filesystems (permissions for
directories and files).
"""

import logging
import os
import tempfile
import unittest

from unittest import mock

from pathlib import Path

from eljef.core import fops

logging.disable(logging.ERROR)


def _cleanup(*args) -> None:
    for p in args:
        if os.path.exists(p):
            fops.delete(p)


def _get_empty_file(suffix: str) -> str:
    path = os.path.join(tempfile.gettempdir(), "testFile.{0!s}".format(suffix))
    Path(path).touch()

    return path


def _get_file(data: str, extension: str) -> str:
    fd, path = tempfile.mkstemp(extension, None, tempfile.gettempdir(), True)
    os.write(fd, data.encode('UTF-8'))
    os.close(fd)

    return path


# noinspection PyBroadException
class TestBackupPath(unittest.TestCase):
    def test_backup_path(self):
        path = _get_empty_file('tmp')
        expected = "{0!s}.bak".format(path)

        fops.backup_path(path)

        try:
            self.assertTrue(os.path.isfile(expected))
            _cleanup(expected, path)
        except Exception:
            _cleanup(expected, path)
            raise

    def test_backup_path_multiple_files(self):
        path = _get_empty_file('tmp')
        path2 = _get_empty_file("tmp.bak")
        path3 = _get_empty_file("tmp.bak.1")
        expected = "{0!s}.bak.2".format(path)

        fops.backup_path(path)

        try:
            self.assertTrue(os.path.isfile(expected))
            _cleanup(expected, path, path2, path3)
        except Exception:
            _cleanup(expected, path, path2, path3)
            raise


# noinspection PyBroadException
class TestDelete(unittest.TestCase):
    def test_delete_exception(self):
        path = _get_empty_file('tmp')

        try:
            with mock.patch('os.remove', new=mock.Mock(side_effect=OSError(5, 'test'))):
                self.assertRaises(OSError, fops.delete, path)
        except Exception:
            _cleanup(path)
            raise

        _cleanup(path)

    def test_delete_path_does_not_exist(self):
        raised = False
        path = os.path.join(tempfile.gettempdir(), "hopefully_this_file_does_not_exist.tmp")

        try:
            fops.delete(path)
        except Exception:
            raised = True

        self.assertFalse(raised)

    def test_delete_symlink_only(self):
        path = _get_empty_file('tmp')
        link = "{0!s}.lnk".format(path)
        os.symlink(path, link)

        fops.delete(link)

        try:
            self.assertFalse(os.path.exists(link))
            _cleanup(link, path)
        except Exception:
            _cleanup(link, path)
            raise

    def test_delete_symlink_backup(self):
        path = _get_empty_file('tmp')
        link = "{0!s}.lnk".format(path)
        os.symlink(path, link)

        fops.delete(link, follow=True, backup=True)

        try:
            self.assertFalse(os.path.exists(link))
            self.assertTrue(os.path.isfile(path))
            _cleanup(link, path)
        except Exception:
            _cleanup(link, path)
            raise

    def test_delete_symlink_and_parent(self):
        path = _get_empty_file('tmp')
        link = "{0!s}.lnk".format(path)
        os.symlink(path, link)

        fops.delete(link, follow=True)

        try:
            self.assertFalse(os.path.exists(link))
            self.assertFalse(os.path.exists(path))
            _cleanup(link, path)
        except Exception:
            _cleanup(link, path)
            raise

    def test_delete_backup(self):
        path = _get_empty_file('tmp')
        expected = "{0!s}.bak".format(path)

        fops.delete(path, backup=True)

        try:
            self.assertFalse(os.path.exists(path))
            self.assertTrue(os.path.exists(expected))
            _cleanup(path, expected)
        except Exception:
            _cleanup(path, expected)
            raise

    def test_delete_directory(self):
        path = os.path.join(tempfile.gettempdir(), "testDir")
        os.mkdir(path)

        fops.delete(path)

        try:
            self.assertFalse(os.path.exists(path))
        except Exception:
            _cleanup(path)
            raise

    def test_delete_file(self):
        path = _get_empty_file('tmp')

        fops.delete(path)

        try:
            self.assertFalse(os.path.exists(path))
            _cleanup(path)
        except Exception:
            _cleanup(path)
            raise


class TestFileRead(unittest.TestCase):
    def test_file_read_no_strip(self):
        data = """test file data
        test file new line

        """
        path = _get_file(data, ".tmp")

        got = fops.file_read(path)
        os.remove(path)

        self.assertEqual(data, got)

    def test_file_read_strip(self):
        data = """test file data
        test file new line

        """
        path = _get_file(data, ".tmp")

        got = fops.file_read(path, True)
        os.remove(path)

        self.assertEqual(data.strip(), got)


class TestFileReadConvert(unittest.TestCase):
    def test_file_read_convert_unknown_type(self):
        self.assertRaises(ValueError, fops.file_read_convert, 'no_path', 'unknown_type')

    def test_file_read_convert_file_does_not_exist(self):
        self.assertRaises(FileNotFoundError, fops.file_read_convert, 'should_not_exist_hopefully_maybe', fops.JSON)

    def test_file_read_convert_not_file(self):
        self.assertRaises(IOError, fops.file_read_convert, tempfile.gettempdir(), fops.JSON)

    def test_file_read_convert_file_does_not_exist_get_default(self):
        want = dict()

        got = fops.file_read_convert("should_not_exist_hopefully_maybe", fops.JSON, default=True)

        self.assertDictEqual(got, want)

    def test_file_read_convert_json(self):
        data = """{
            "test": "test"
        }
        """
        want = {
            'test': 'test'
        }
        path = _get_file(data, ".json")

        got = fops.file_read_convert(path, fops.JSON)
        os.remove(path)

        self.assertDictEqual(got, want)

    def test_file_read_convert_kv(self):
        data = """test=test
        """
        want = {
            'test': 'test'
        }
        path = _get_file(data, ".tmp")

        got = fops.file_read_convert(path, fops.KV)
        os.remove(path)

        self.assertDictEqual(got, want)

    def test_file_read_convert_xml(self):
        data = """<?xml version="1.0"?>
            <test>test</test>
        """
        want = {
            'test': 'test'
        }
        path = _get_file(data, ".xml")

        got = fops.file_read_convert(path, fops.XML)
        os.remove(path)

        self.assertDictEqual(got, want)

    def test_file_read_convert_yaml(self):
        data = '''test: "test"'''
        want = {
            'test': 'test'
        }
        path = _get_file(data, ".yml")

        got = fops.file_read_convert(path, fops.YAML)
        os.remove(path)

        self.assertDictEqual(got, want)


# noinspection PyBroadException
class TestFileWrite(unittest.TestCase):
    def test_file_write_file_does_not_exist(self):
        data = """test data"""
        path = os.path.join(tempfile.gettempdir(), "testFile.tmp")

        fops.file_write(path, data, newline='\n')

        try:
            self.assertTrue(os.path.isfile(path))
        except Exception:
            _cleanup(path)
            raise

        got = fops.file_read(path, strip=True)
        _cleanup(path)

        self.assertEqual(data, got)

    def test_file_write_file_exists(self):
        data = """test data"""
        path = _get_file("testing data", ".tmp")

        fops.file_write(path, data, newline='\n')

        got = fops.file_read(path, strip=True)
        _cleanup(path)

        self.assertEqual(data, got)

    def test_file_write_with_backup(self):
        data = """test data"""
        path = _get_file("testing data", ".tmp")
        expected = "{0!s}.bak".format(path)

        fops.file_write(path, data, backup=True, newline='\n')

        try:
            self.assertTrue(os.path.isfile(expected))
        except Exception:
            _cleanup(path, expected)
            raise

        got = fops.file_read(path, strip=True)
        _cleanup(path, expected)

        self.assertEqual(data, got)


class TestFileWriteCovertDefaults(unittest.TestCase):
    def test_file_write_convert_defaults_unknown_type(self):
        self.assertRaises(ValueError, fops.file_write_convert_defaults, 'unknown')

    def test_file_write_convert_defaults(self):
        tests = {
            fops.JSON: {'indent': 4},
            fops.KV: {'spaced': False},
            fops.XML: {'pretty': True, 'full_document': True, 'indent': '    '},
            fops.YAML: {'default_flow_style': False}
        }
        for key, value in tests.items():
            got = fops.file_write_convert_defaults(key)
            self.assertDictEqual(value, got, msg=key)


# noinspection PyBroadException
class TestFileWriteConvert(unittest.TestCase):
    def test_file_write_convert(self):
        data = {"test": "test"}
        tests = {
            fops.JSON: '{\n    "test": "test"\n}',
            fops.KV: 'test=test',
            fops.XML: '<?xml version="1.0" encoding="utf-8"?>\n<test>test</test>',
            fops.YAML: 'test: test'
        }
        for key, value in tests.items():
            path = os.path.join(tempfile.gettempdir(), "tempFile.{0!s}".format(key))
            args = fops.file_write_convert_defaults(key)
            fops.file_write_convert(path, key, data, dumper_args=args)

            try:
                self.assertTrue(os.path.isfile(path))
            except Exception:
                _cleanup(path)
                raise

            got = fops.file_read(path, strip=True)
            _cleanup(path)

            self.assertEqual(value, got, msg=key)


class TestPushd(unittest.TestCase):
    def test_pushd_directory_does_not_exist(self):
        def child():
            with fops.pushd('something_that_should_not_exist'):
                print('')
        self.assertRaises(FileNotFoundError, child)

    def test_pushd(self):
        data = 'pushd test data'
        path = os.path.join(tempfile.gettempdir(), 'testFile.tmp')

        with fops.pushd(tempfile.gettempdir()):
            fops.file_write('testFile.tmp', data)

        got = fops.file_read(path, True)
        _cleanup(path)

        self.assertEqual(data, got)


if __name__ == '__main__':
    unittest.main()
