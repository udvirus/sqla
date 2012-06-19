#!/usr/bin/python
# coding: utf-8
from bottle import HTTPError,\
                   PluginError
from sqlalchemy.orm import sessionmaker,\
                           scoped_session
from sqlalchemy.exc import SQLAlchemyError
from . import engine

class SQLAlchemyPlugin(object):
    name = 'sqlalchemy'
    api = '2'

    def __init__(self, engine, keyword='db', autoflush=False, autocommit=False):
        self.engine = engine
        self.keyword = keyword
        self.autoflush = autoflush
        self.autocommit = autocommit

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, SQLAlchemyPlugin): continue

            if other.keyword == self.keyword:
                raise PluginError('Found another sqlalchemy plugin with\
                    conflicting settings (non-unfque keyword).')

    def apply(self, callback, context):
        import inspect
        args = inspect.getargspec(context.callback)[0]
        if self.keyword not in args: 
            return callback

        session = scoped_session(sessionmaker(bind=self.engine, autoflush=self.autoflush))
        def warpper(*a, **kw):
            kw[self.keyword] = session
            try:
                rv = callback(*a, **kw)
                if self.autocommit: session.commit()
            except SQLAlchemyError, e:
                session.rollback()
                raise HTTPError(500, e)
            finally:
                session.close()
            return rv
        return warpper

plugin_sqlalchemy = SQLAlchemyPlugin(engine=engine, autocommit=False)
