#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name,redefined-builtin
"""Sphinx Configuration for ElJef Core"""

import sys
import os


FILE_PATH = os.path.dirname(os.path.abspath(os.path.join(__file__, '../..')))
sys.path.insert(0, FILE_PATH)

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
add_module_names = False

project = 'ElJef Core'
# noinspection PyShadowingBuiltins
copyright = '2016, Jef Oliver'
author = 'Jef Oliver'

version = '1.1.1'
release = '1.1.1'

language = None

exclude_patterns = []

pygments_style = 'sphinx'

todo_include_todos = False


html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'ElJefCoredoc'
html_sidebars = {'**': ['indexsidebar.html', 'searchbox.html']}

latex_elements = {}
latex_documents = [
    (master_doc, 'ElJefCore.tex', 'ElJef Core Documentation',
     'Jef Oliver', 'manual'),
]

texinfo_documents = [
    (master_doc, 'ElJefCore', 'ElJef Core Documentation', author,
     'ElJefCore', 'ElJef Core functionality.', 'Miscellaneous'),
]
