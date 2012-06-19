#!/usr/bin/python
# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,\
                           sessionmaker
from sqlalchemy.engine.url import URL

class SqlaException(Exception):
    pass

class Sqla(object):
    DB_CONFS = None
    DEBUG = None

    engines = {}
    connects = {}
    sessions = {}

    def __init__(self, settings, db_conf, ekw={}, skw={}, *a, **kw):
        """ Initialize GameCC Sqla Model

        Args:
            settings: Database config settings
            db_conf: default database config name
            ekw: default database engine kwargs
            skw: default database session kwargs
        """
        if not hasattr(settings, 'DB_CONFS'):
            raise SqlaException('Can not find Database Setting in the settings file.')
        self.DB_CONFS = getattr(settings, 'DB_CONFS', None)
        self.DEBUG = getattr(settings, 'DB_DEBUG', False)
        self.__call__(db_conf, ekw=ekw, skw=skw, *a, **kw)

    def __call__(self, db_conf, ekw={}, skw={}, *a, **kw):
        """
        """
        if db_conf in self.DB_CONFS:
            self.connects[db_conf] = URL(**self.DB_CONFS[db_conf])
            self.engines[db_conf] = create_engine(self.connects[db_conf],
                    echo=self.DEBUG, **ekw)
            self.sessions[db_conf] = scoped_session(sessionmaker(
                bind=self.engines[db_conf], **skw))
        else:
            raise SqlaException('Unknow database config')
