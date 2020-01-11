# -*- coding: UTF-8 -*-
# Copyright (c) 2017-2020, Jef Oliver
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
# test_merge.py : ElJef Merge Testing
"""ElJef Merge Testing

ElJef merge testing functionality.
"""

import logging
import unittest

from eljef.core import merge

logging.disable(logging.ERROR)


class TestMergeDictionaries(unittest.TestCase):
    def test_merge_dictionaries(self):
        tests = [
            {
                'dict_a': dict(),
                'dict_b': {
                    'test': 'test'
                },
                'want': {
                    'test': 'test'
                }
            },
            {
                'dict_a': {
                    'test': 'test2'
                },
                'dict_b': {
                    'test': 'test'
                },
                'want': {
                    'test': 'test'
                }
            },
            {
                'dict_a': {
                    'test': {
                        'test2': dict(),
                    }
                },
                'dict_b': {
                    'test': {
                        'test2': ['test', 'test']
                    }
                },
                'want': {
                    'test': {
                        'test2': ['test', 'test']
                    }
                }
            },
            {
                'dict_a': {
                    'test': {
                        'test2': {
                            'test3': 'test4'
                        }
                    }
                },
                'dict_b': {
                    'test': {
                        'test2': {
                            'test5': {
                                'test6': 'test7'
                            }
                        }
                    },
                    'test8': {
                        'test9': 'test10'
                    }
                },
                'want': {
                    'test': {
                        'test2': {
                            'test3': 'test4',
                            'test5': {
                                'test6': 'test7'
                            },
                        },
                    },
                    'test8': {
                        'test9': 'test10'
                    }
                }
            }
        ]
        for test in tests:
            got = merge.merge_dictionaries(test['dict_a'], test['dict_b'])
            self.assertDictEqual(got, test['want'])


if __name__ == '__main__':
    unittest.main()
