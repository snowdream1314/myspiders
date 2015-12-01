#!c:\users\cb-ye\my_workspace\myspiders\virtualenvs\env1\scripts\python.exe
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
tap2deb
"""
import sys

try:
    __import__('_preamble')
except ImportError:
    sys.exc_clear()

from twisted.scripts import tap2deb
tap2deb.run()
