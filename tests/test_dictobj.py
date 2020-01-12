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
# test_dictobj.py : Dictionary Object Testing
"""ElJef Dictionary Object Testing

This module holds the tests for the Dictionary Object class.
"""

import logging
import unittest

from eljef.core import dictobj

logging.disable(logging.ERROR)


class TestDictObj(unittest.TestCase):
    @staticmethod
    def _return_dictobj() -> dictobj.DictObj:
        data = {
            'test': 'test',
            'test2': {
                'test3': 'test3'
            }
        }
        return dictobj.DictObj(data)

    def test_dictobj_contains(self):
        d = self._return_dictobj()
        self.assertTrue('test' in d)

    def test_dictobj_iter(self):
        test_iter = iter(self._return_dictobj())
        self.assertTrue(next(test_iter) is not None)

    def test_dictobj_delattr(self):
        d = self._return_dictobj()
        delattr(d, 'test')
        self.assertFalse(hasattr(d, 'test'))

    def test_dictobj_delattr_exception(self):
        d = self._return_dictobj()
        self.assertRaises(AttributeError, delattr, d, 'not_there')

    def test_dictobj_getattr(self):
        d = self._return_dictobj()
        t = getattr(d, 'test')
        self.assertEqual('test', t)

    def test_dictobj_getattr_exception(self):
        d = self._return_dictobj()
        self.assertRaises(AttributeError, getattr, d, 'not_there')

    def test_dictobj_delitem(self):
        d = self._return_dictobj()
        del(d['test'])
        self.assertTrue('test' not in d)

    def test_dictobj_getitem(self):
        d = self._return_dictobj()
        self.assertEqual('test', d['test'])

    def test_dictobj_len(self):
        self.assertTrue(len(self._return_dictobj()) > 0)

    def test_dictobj_repr(self):
        d = self._return_dictobj()
        self.assertTrue(len(repr(d)) > 0)

    def test_dictobj_setattr(self):
        d = self._return_dictobj()
        setattr(d, 'test4', 'test4')
        self.assertTrue(d.test4 == 'test4')

    def test_dictobj_setitem(self):
        d = self._return_dictobj()
        d['test4'] = 'test4'
        self.assertTrue(d.test4 == 'test4')

    def test_dictobj_pop(self):
        want = {
            'test': 'test'
        }
        want2 = {
            'test3': 'test3'
        }
        d = self._return_dictobj()
        got2 = d.pop('test2').to_dict()
        got = d.to_dict()
        self.assertDictEqual(want, got)
        self.assertDictEqual(want2, got2)

        self.assertRaises(KeyError, d.pop, 'test3')

        got = d.pop('test4', 'test9')
        self.assertEqual(got, 'test9')

    def test_dictobj_to_dict(self):
        want = {
            'test': 'test',
            'test2': {
                'test3': 'test3'
            }
        }
        d = self._return_dictobj()
        got = d.to_dict()
        self.assertDictEqual(want, got)

    def test_dictobj_update(self):
        d = self._return_dictobj()
        d.update({'new_test': 'test'})
        self.assertEqual(d.new_test, 'test')


if __name__ == '__main__':
    unittest.main()
