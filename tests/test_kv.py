# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""ElJef Key/Value Reading/Writing Testing"""

import logging
import unittest

from eljef.core import kv

logging.disable(logging.ERROR)


class TestDumps(unittest.TestCase):
    def test_dumps_no_spaces(self):
        input_data = {
            'test': 'test'
        }
        want = 'test=test'
        got = kv.dumps(input_data)
        self.assertEqual(want, got)

    def test_dumps_spaces(self):
        input_data = {
            'test': 'test'
        }
        want = 'test = test'
        got = kv.dumps(input_data, spaced=True)
        self.assertEqual(want, got)

    def test_dumps_with_multiple_lines(self):
        input_data = {
            'test': 'test',
            'test2': 'test2',
            'test3': 'test3'
        }
        want = 'test=test\ntest2=test2\ntest3=test3'
        got = kv.dumps(input_data)
        self.assertEqual(want, got)

    def test_dumps_with_dictionary(self):
        input_data = {
            'test': 'test',
            'test2': {
                'test3': 'test3'
            }
        }
        self.assertRaises(TypeError, kv.dumps, input_data)


class TestLoads(unittest.TestCase):
    def test_loads_no_comments_no_spaces(self):
        input_data = 'test=test\ntest2=test2'
        want = {
            'test': 'test',
            'test2': 'test2'
        }
        got = kv.loads(input_data)
        self.assertDictEqual(want, got)

    def test_loads_no_comments_spaces(self):
        input_data = 'test = test\ntest2 = test2'
        want = {
            'test': 'test',
            'test2': 'test2'
        }
        got = kv.loads(input_data)
        self.assertDictEqual(want, got)

    def test_loads_no_comments_stupid_spaces(self):
        input_data = 'test =     test\ntest2     =   test2'
        want = {
            'test': 'test',
            'test2': 'test2'
        }
        got = kv.loads(input_data)
        self.assertDictEqual(want, got)

    def test_loads_no_comments_mixed_spaces(self):
        input_data = 'test = test\ntest2=test2'
        want = {
            'test': 'test',
            'test2': 'test2'
        }
        got = kv.loads(input_data)
        self.assertDictEqual(want, got)

    def test_loads_comments(self):
        input_data = ''';comment
        # comment
        / comment
        test=test
        # commented out pair test2=test3
        test2=test2
        '''
        want = {
            'test': 'test',
            'test2': 'test2'
        }
        got = kv.loads(input_data)
        self.assertDictEqual(want, got)

    def test_loads_inline_comments(self):
        input_data = ''';comment
        # comment
        / comment
        test=test
        # commented out pair test2=test3
        test2=test2
        test3=test3 # inline comment
        '''
        want = {
            'test': 'test',
            'test2': 'test2',
            'test3': 'test3'
        }
        got = kv.loads(input_data, comment='#')
        self.assertDictEqual(want, got)


if __name__ == '__main__':
    unittest.main()
