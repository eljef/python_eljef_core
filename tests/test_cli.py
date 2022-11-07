# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""ElJef Application CLI Functions"""

import contextlib
import io
import os
import sys
import unittest

from unittest.mock import patch

from eljef.core import cli


class TestArgsSimple(unittest.TestCase):
    def test_args_simple(self):
        arg_list1 = [cli.Arg(['-z', '--zz'], {'dest': 'zz'})]
        arg_list2 = [cli.Arg(['--zz'], {'dest': 'zz'})]

        test_args = ['test_prog', '-z', 'test1']
        with patch.object(sys, 'argv', test_args):
            got = cli.args_simple('prog_name', 'prog_desc', arg_list1, exit_on_error=False)
            self.assertTrue(got.zz == 'test1', 'zz != test1')

        test_args = ['test_prog', '--zz', 'test2']
        with patch.object(sys, 'argv', test_args):
            got = cli.args_simple('prog_name', 'prog_desc', arg_list1, exit_on_error=False)
            self.assertTrue(got.zz == 'test2', 'zz != test2')

        test_args = ['test_prog', '--zz', 'test3']
        with patch.object(sys, 'argv', test_args):
            got = cli.args_simple('prog_name', 'prog_desc', arg_list2, exit_on_error=False)
            self.assertTrue(got.zz == 'test3', 'zz != test3')


class TestPrintVersion(unittest.TestCase):
    def test_print_version(self):
        new_out = io.StringIO()
        with contextlib.redirect_stdout(new_out):
            self.assertRaises(SystemExit, cli.print_version, 'Test', '0.0.1')

        output = new_out.getvalue()
        self.assertEqual(f"Test - 0.0.1{os.linesep}", output)


if __name__ == '__main__':
    unittest.main()
