# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""ElJef Merge Testing"""

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
