#!/usr/bin/python
# coding: utf-8

from sqlalchemy import and_
try:from orm import SiteModel
except ImportError: from sqla.orm import SiteModel

class ObjectTypeError(Exception): pass
