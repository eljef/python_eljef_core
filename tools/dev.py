#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Development Helper"""

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys

# Needed Information
CLEANUP_DIRS = ['build', 'dist', 'eljef_core.egg-info']
DIR_TOOLS = 'tools'
INSTALL_CMD = [sys.executable, 'setup.py', 'install']
LINT_DIRS = ['eljef/core']
LINT_TOOLS = ['flake8', 'pylint']
VERSION_INFO = {
    'main': 'eljef/core/__version__.py',
    'name': 'VERSION',
    'files': ['eljef/core/__version__.py', 'docs/source/conf.py', 'setup.py']
}

# Error Messages
ERR_INSTALL_FAIL = 'Installation failed. Run -cleanup and try again.'
ERR_UNSUPPORTED_VERSION = 'ElJef tools only supports python major version 3 and minor version 6 or higher.'
ERR_RUN_FROM_BASE = 'Run this script from the root of the source tree as "python tools/dev.py"'
ERR_TOOL_INSTALL = "Please install required tools."
ERR_TOOL_MISSING = "Required tool not found: {0}"


def arg_parse() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Development Helper')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-cleanup', dest='do_cleanup', action='store_true',
                       help='cleanup any remnants of the installation process')
    group.add_argument('-install', dest='do_install', action='store_true',
                       help='install the current project')
    group.add_argument('-lint', dest='do_lint', action='store_true',
                       help='run linting for this project')
    group.add_argument('-version_current', dest='version_get', action='store_true',
                       help='return the current project version')
    group.add_argument('-version_set', dest='version_set', type=str,
                       help='sets the project version to the provided value')

    args = parser.parse_args()

    return args


def check_lint_tools() -> bool:
    """check if linting tools are installed"""
    missing = False

    for tool in LINT_TOOLS:
        if not shutil.which(tool):
            print(ERR_TOOL_MISSING.format(tool) + '\n')
            missing = True

    return missing


def check_version() -> bool:
    """check the python version"""
    return sys.version_info[0] == 3 and sys.version_info[1] >= 6


def check_dir():
    """check if the specified tools directory exists"""
    return os.path.isdir(DIR_TOOLS)


def current_version() -> str:
    """return the current version of the project"""
    m_name = VERSION_INFO['main'].replace('/', '.').replace('.py', '')
    module_spec = importlib.util.spec_from_file_location(m_name, VERSION_INFO['main'])
    load = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(load)

    return getattr(load, VERSION_INFO['name'])


def do_cleanup():
    """cleanup installation artifacts"""
    for directory in CLEANUP_DIRS:
        shutil.rmtree(directory)


def do_lint():
    """run linting tools"""
    for tool in LINT_TOOLS:
        cmd = [tool] + LINT_DIRS
        print(' '.join(cmd))
        subprocess.run(cmd)
        print('\n')


def do_install():
    """install the project"""
    completed = subprocess.run(INSTALL_CMD)
    if completed.returncode != 0:
        raise SystemExit(ERR_INSTALL_FAIL)


def do_version_get():
    """print the current project version"""
    print('Current Project Version: ' + current_version())


def do_version_set(new_version: str):
    """set a new version for the project"""
    current = current_version()

    print('Bumping Project Version: ' + current + ' -> ' + new_version)

    for version_file in VERSION_INFO['files']:
        with open(version_file, 'r+', newline='\n') as open_file:
            data = open_file.read()
            open_file.seek(0)
            open_file.write(data.replace(current, new_version))
            open_file.truncate()
            open_file.close()


def run():
    """run commands based on provided arguments"""
    args = arg_parse()

    if args.do_cleanup:
        do_cleanup()
    elif args.do_lint:
        do_lint()
    elif args.do_install:
        do_install()
    elif args.version_get:
        do_version_get()
    else:
        do_version_set(args.version_set)


def main():
    """do basic checks and then execute based on provided arguments"""
    if not check_version():
        raise SystemExit(ERR_UNSUPPORTED_VERSION)
    if not check_dir():
        raise SystemExit(ERR_RUN_FROM_BASE)
    if check_lint_tools():
        raise SystemExit(ERR_TOOL_INSTALL)

    run()


if __name__ == "__main__":
    main()
