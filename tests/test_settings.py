# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""ElJef Settings Handling"""

import logging
import os
import tempfile
import unittest

from eljef.core.settings import Settings

logging.disable(logging.ERROR)


class TestSettings(unittest.TestCase):
    @staticmethod
    def _get_file(data: str) -> str:
        fd, path = tempfile.mkstemp(".yaml", None, tempfile.gettempdir(), True)
        os.write(fd, data.encode('UTF-8'))
        os.close(fd)

        return path

    def test_init_settings_files_dont_exist(self):
        defaults = {
            'test': 'test'
        }

        t = Settings(defaults, '', '')
        got = t.get_all()
        self.assertDictEqual(got, defaults)

    def test_init_only_user_file(self):
        defaults = {
            'test': 'test'
        }
        want = {
            'test': 'test',
            'user': 'user'
        }

        path = self._get_file("{'user': 'user'}")
        t = Settings(defaults, path, '')
        os.remove(path)

        got = t.get_all()
        self.assertDictEqual(got, want)

    def test_init_only_system_file(self):
        defaults = {
            'test': 'test'
        }
        want = {
            'test': 'test',
            'sys': 'sys'
        }

        path = self._get_file("{'sys': 'sys'}")
        t = Settings(defaults, path, '')
        os.remove(path)

        got = t.get_all()
        self.assertDictEqual(got, want)

    def test_init_user_and_system_file(self):
        defaults = {
            'test': 'test'
        }
        want = {
            'test': 'test',
            'sys': 'sys',
            'user': 'user',
        }

        s_path = self._get_file("{'sys': 'sys'}")
        u_path = self._get_file("{'user': 'user'}")
        t = Settings(defaults, u_path, s_path)
        os.remove(s_path)
        os.remove(u_path)

        got = t.get_all()
        self.assertDictEqual(got, want)

    def test_get(self):
        t = Settings({'test': 'test'}, '', '')
        got = t.get('test')
        self.assertEqual('test', got)

    def test_get_all(self):
        defaults = {
            'test': 'test'
        }
        t = Settings(defaults, '', '')
        got = t.get_all()
        self.assertDictEqual(defaults, got)

    def test_read(self):
        want = {
            'test': 'test'
        }

        path = self._get_file("{'test': 'test'}")
        got = Settings.read(path, '')
        os.remove(path)
        self.assertDictEqual(want, got)


if __name__ == '__main__':
    unittest.main()
