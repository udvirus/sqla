#!/usr/bin/python
# coding: utf-8
""" GameCC SQLAlchemy Packages
"""
__version__ = '0.0.1'

import os
import sys
import imp
from .base import Sqla

try:
    imp.find_module('settings')
except ImportError:
    sys.path.insert(os.path.dirname(os.path.abspath(__file__)), 0)

import settings


sqla = Sqla(settings, 'default')
engine = sqla.engines['default']
session = sqla.sessions['default']
