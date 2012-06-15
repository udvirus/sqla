#!/usr/bin/python
# coding: utf-8

try:
    import settings
    DATABASE_SETTING    = settings.DATABASE_SETTING
    DATABASE_DEBUG      = settings.DEBUG
except ImportError:
    DATABASE_DEBUG      = True
    DATABASE_SETTING    = {
        'drivername': 'mysql',
        'username': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': '3306',
        'database': 'valor',
        'query': {'charset': 'utf8'},
    }

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker

CONNECT_STRING = URL(**DATABASE_SETTING)
engine = create_engine(CONNECT_STRING, echo=DATABASE_DEBUG)
#Session = sessionmaker(bind=engine)()
Session = scoped_session(sessionmaker(bind=engine, autoflush=False))
