#!/usr/bin/python
# coding: utf-8

from sqlalchemy import Table, Column, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR, BOOLEAN, TEXT, DECIMAL

metadata    = MetaData()

user_base = Table('user_base', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('email', VARCHAR(128), unique=True, nullable=False),
    Column('username', VARCHAR(32), unique=True, nullable=False),
    Column('password', VARCHAR(64), nullable=False),
    Column('secret', VARCHAR(32), nullable=False), # salt
    Column('actived', BOOLEAN, nullable=False, default=0), # user active 
    Column('active_token', VARCHAR(32), index=True), # user active link
    Column('login_sequence', VARCHAR(32), index=True), # login_sequence
    Column('login_token', VARCHAR(32), index=True), # login_token
    Column('admin', BOOLEAN, nullable=False, default=0),
    Column('root', BOOLEAN, nullable=False, default=0),
    Column('_last_login', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_login_addr', INTEGER(unsigned=True), nullable=False),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_profile = Table('user_profile', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('thumb', VARCHAR(64)),
    Column('nickname', VARCHAR(16)), 
    Column('gender', TINYINT(unsigned=True), nullable=False, default=2),
    Column('_birthday', INTEGER(unsigned=True)),
    Column('first_name', VARCHAR(32)) ,
    Column('last_name', VARCHAR(32)),
    Column('cellphone', VARCHAR(16)),
    Column('country', VARCHAR(256)),
    Column('province', VARCHAR(256)),
    Column('city', VARCHAR(256)),
    Column('address', VARCHAR(256)), 
    Column('website', VARCHAR(256)),
    Column('introduction', VARCHAR(256)),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_relation = Table('user_relation', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('target_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('type', BOOLEAN, nullable=False, default=True),
    UniqueConstraint('user_id', 'target_id', 'type'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_friendtag = Table('user_friendtag', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('name', VARCHAR(32), nullable=False, index=True),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_friendsgroup = Table('user_friendsgroup', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('friendtag_id', INTEGER(unsigned=True), ForeignKey('user_friendtag.id'), nullable=False),
    Column('friend_id', INTEGER(unsigned=True), ForeignKey('user_profile.user_id'), nullable=False),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_message = Table('user_message', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('target_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('read', BOOLEAN, nullable=False, default=0),
    Column('title', VARCHAR(32), nullable=False),
    Column('content', TEXT, nullable=False),
    UniqueConstraint('user_id', 'target_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_album = Table('user_album', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('name', VARCHAR(32), nullable=False),
    Column('excerpt', VARCHAR(256)),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_image = Table('user_image', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('servname', VARCHAR(32), nullable=False, unique=True),
    Column('basename', VARCHAR(64), nullable=False),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_album_image = Table('user_album_image', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('album_id', INTEGER(unsigned=True), ForeignKey('user_album.id'), nullable=False),
    Column('image_id', INTEGER(unsigned=True), ForeignKey('user_image.id'), nullable=False),
    Column('alias', VARCHAR(32)),
    Column('description', TEXT),
    UniqueConstraint('album_id', 'image_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_event = Table('user_event', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('show', BOOLEAN, nullable=False, default=0), # show this event
    Column('object_type_id', TINYINT(unsigned=True), nullable=False),
    Column('object_pk', INTEGER(unsigned=True), nullable=False),
    Column('message', VARCHAR(256)), #TEXT
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

news_category = Table('news_category', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('name', VARCHAR(16), nullable=False, unique=True),
    Column('segment', VARCHAR(128), nullable=False, unique=True), 
    Column('sort', INTEGER, nullable=False, default=0),
    Column('description', TEXT),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

news_detail = Table('news_detail', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('author_id', INTEGER(unsigned=True), ForeignKey('user_profile.user_id'), nullable=False),
    Column('author', VARCHAR(32)), # user_profile.nickname
    Column('category_id', INTEGER(unsigned=True), ForeignKey('news_category.id'), nullable=False),
    Column('headline', VARCHAR(64), nullable=False, index=True),
    Column('published', BOOLEAN, nullable=False, default=0),
    Column('enable_comment', BOOLEAN, nullable=False, default=1),
    Column('publication_data', INTEGER(unsigned=True)),
    Column('thumb', VARCHAR(64)),
    Column('excerpt', VARCHAR(256)),
    Column('visits', INTEGER(unsigned=True), nullable=False, default=1),
    Column('comments', INTEGER(unsigned=True), nullable=False, default=0),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

news_content = Table('news_content', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('news_id', INTEGER(unsigned=True), ForeignKey('news_detail.id'), nullable=False),
    Column('content', TEXT, nullable=False),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)


game_category = Table('game_category', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('name', VARCHAR(16), nullable=False, unique=True),
    Column('segment', VARCHAR(128), nullable=False, unique=True), 
    Column('sort', INTEGER, nullable=False, default=0),
    Column('description', TEXT),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_platform = Table('game_platform', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('name', VARCHAR(32), nullable=False, unique=True),
    Column('segment', VARCHAR(128), nullable=False, unique=True), 
    Column('alias', VARCHAR(64)),
    Column('sort', INTEGER, nullable=False, default=0),
    Column('description', TEXT),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_detail = Table('game_detail', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('category_id', INTEGER(unsigned=True), ForeignKey('game_category.id'), nullable=False),
    Column('author_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('name', VARCHAR(128), nullable=False), # X
    Column('alias', VARCHAR(128)),
    Column('published', BOOLEAN, nullable=False, default=0),
    Column('publication_date', INTEGER(unsigned=True)),
    Column('thumb', VARCHAR(64)),
    Column('excerpt', VARCHAR(256)),
    Column('developer', VARCHAR(128)),
    Column('developer_site', VARCHAR(256)),
    # count how many people interest/playing/played
    # x #
    Column('interest', INTEGER(unsigned=True), nullable=False, default=0),
    Column('playing', INTEGER(unsigned=True), nullable=False, default=0),
    Column('played', INTEGER(unsigned=True), nullable=False, default=0),
    # count how many peopler evaluation this game, and total scores
    Column('counter', INTEGER(unsigned=True), nullable=False, default=0),
    Column('graph', INTEGER(unsigned=True), nullable=False, default=0),
    Column('control', INTEGER(unsigned=True), nullable=False, default=0),
    Column('ploy', INTEGER(unsigned=True), nullable=False, default=0),
    Column('opera', INTEGER(unsigned=True), nullable=False, default=0),
    Column('music', INTEGER(unsigned=True), nullable=False, default=0),
    # x #
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_content = Table('game_content', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),
    Column('content', TEXT),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_infomation = Table('game_infomation', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('platform_id', INTEGER(unsigned=True), ForeignKey('game_platform.id'), nullable=False),
    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),
    Column('currency_cny', DECIMAL(precision=8, scale=2), nullable=False, default=0),
    Column('currency_usd', DECIMAL(precision=8, scale=2), nullable=False, default=0),
    Column('discount', TINYINT(unsigned=True), nullable=False, index=True, default=100),
    Column('market_url', VARCHAR(256), nullable=False),
    Column('system_require', VARCHAR(64)), # TINYTEXT
    Column('capacity', INTEGER(unsigned=True)),
    Column('language', VARCHAR(32)),
    Column('version', VARCHAR(32)),
    Column('_upgrade', INTEGER(unsigned=True)), #
    Column('roles', TEXT), # x
    Column('downloads', TEXT), # str([(DownloadSiteName, DownloadURL),])
    Column('log', TEXT),
    # count how many people interest/playing/played
    Column('interest', INTEGER(unsigned=True), nullable=False, default=0),
    Column('playing', INTEGER(unsigned=True), nullable=False, default=0),
    Column('played', INTEGER(unsigned=True), nullable=False, default=0),
    # count how many peopler evaluation this game, and total scores
    Column('counter', INTEGER(unsigned=True), nullable=False, default=0),
    Column('graph', INTEGER(unsigned=True), nullable=False, default=0),
    Column('control', INTEGER(unsigned=True), nullable=False, default=0),
    Column('ploy', INTEGER(unsigned=True), nullable=False, default=0),
    Column('opera', INTEGER(unsigned=True), nullable=False, default=0),
    Column('music', INTEGER(unsigned=True), nullable=False, default=0),
    UniqueConstraint('platform_id', 'game_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

# game mark
game_mark = Table('game_evaluation', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),
    # game mark
    Column('mark', BOOLEAN, nullable=False, default=0),
    Column('interest', BOOLEAN, nullable=False, default=0),
    Column('playing', BOOLEAN, nullable=False, default=0),
    Column('played', BOOLEAN, nullable=False, default=0),
    #Column('start_date', INTEGER(unsigned=True)), # start play (&2)
    #Column('deadline', INTEGER(unsigned=True)), # end play (&2)
    # game score
    Column('score', BOOLEAN, nullable=False, default=0),
    Column('graph', TINYINT(unsigned=True), nullable=False, default=0),
    Column('control', TINYINT(unsigned=True), nullable=False, default=0),
    Column('ploy', TINYINT(unsigned=True), nullable=False, default=0),
    Column('opera', TINYINT(unsigned=True), nullable=False, default=0),
    Column('music', TINYINT(unsigned=True), nullable=False, default=0),
    # game evaluation content
    Column('commented', BOOLEAN, nullable=False, default=0),
    Column('content', TEXT),
    # how many people agree or disagree this (&2)
    Column('argee', INTEGER(unsigned=True), nullable=False, default=0),
    Column('disargee', INTEGER(unsigned=True), nullable=False, default=0),
    Column('username', VARCHAR(64)),
    Column('user_thumb', VARCHAR(64)), 
    UniqueConstraint('user_id', 'game_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_apply = Table('group_apply', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('applicant', INTEGER(unsigned=True), nullable=False),
    Column('name', VARCHAR(32), nullable=False),
    Column('privacy', BOOLEAN, nullable=False, default=0),
    Column('excerpt', VARCHAR(256), nullable=False),
    Column('remark', TEXT),
    Column('actived', BOOLEAN, nullable=False, default=0),
    Column('deal', BOOLEAN, nullable=False, default=0),
    Column('active_code', VARCHAR(32)),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_detail = Table('group_detail', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('founder_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),   # X
    Column('allow', BOOLEAN, nullable=False, default=0), # X
    Column('privacy', BOOLEAN, nullable=False, default=0),
    Column('name', VARCHAR(32), nullable=False, unique=True),
    Column('thumb', VARCHAR(256)),
    Column('excerpt', VARCHAR(256)),
    #Column('introduction', TEXT),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_game = Table('group_game', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('group_id', INTEGER(unsigned=True), ForeignKey('group_detail.id'), nullable=False),
    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_member = Table('group_member', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('group_id', INTEGER(unsigned=True), ForeignKey('group_detail.id'), nullable=False),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('user_type', TINYINT(unsigned=True), nullable=False, default=1),
    UniqueConstraint('group_id', 'user_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_topic = Table('group_topic', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('group_id', INTEGER(unsigned=True), ForeignKey('group_detail.id'), nullable=False),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('nickname', VARCHAR(64)),
    Column('user_thumb', VARCHAR(64)),
    Column('title', VARCHAR(64), nullable=False),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_discus = Table('group_discus', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('topic_id', INTEGER(unsigned=True), ForeignKey('group_topic.id'), nullable=False),
    Column('nickname', VARCHAR(62)),
    Column('user_thumb', VARCHAR(64)), 
    Column('content', TEXT, nullable=False),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

tag_content = Table('tag_content', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('content', VARCHAR(32), nullable=False, unique=True),
    Column('references', INTEGER(unique=True), default=0),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

tag_mark = Table('tag_mark', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('object_type_id', INTEGER(unsigned=True), ForeignKey('site_model.id'), nullable=False),
    Column('object_pk', INTEGER(unsigned=True), nullable=False),
    Column('tag_id', INTEGER(unsigned=True), ForeignKey('tag_content.id'), nullable=False),
    UniqueConstraint('user_id', 'object_type_id', 'object_pk', 'tag_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

site_model = Table('site_model', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('app_label', VARCHAR(64), nullable=False),
    Column('model', VARCHAR(64), nullable=False),
    UniqueConstraint('app_label', 'model'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

site_seo = Table('site_seo', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('object_type_id', INTEGER(unsigned=True), ForeignKey('site_model.id'), nullable=False),
    Column('object_pk', INTEGER(unsigned=True), nullable=False),
    Column('page_title', VARCHAR(64)),
    Column('page_keyword', VARCHAR(128)),
    Column('page_description', VARCHAR(1024)),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

site_comment = Table('site_comment', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_profile.user_id')),
    Column('show', BOOLEAN, nullable=False, default=True),
    Column('object_type_id', INTEGER(unsigned=True), ForeignKey('site_model.id'), nullable=False),
    Column('object_pk', INTEGER(unsigned=True), nullable=False),
    Column('username', VARCHAR(32)),
    Column('nickname', VARCHAR(64)),
    Column('email', VARCHAR(128)),
    Column('ipaddr', INTEGER(unsigned=True)),
    Column('user_thumb', VARCHAR(64)), # 64
    Column('content', TEXT),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

mods = map(
    lambda x: dict(
        app_label=x.split('_')[0], 
        model=x.split('_', 1)[1],
    ), 
    metadata.tables.keys(),
)

if __name__ == '__main__':
    '''
    from sqlalchemy import create_engine
    from base import engine, DATABASE_SETTING

    test_engine = '%s://%s:%s@%s' % \
        (DATABASE_SETTING['drivername'], DATABASE_SETTING['username'], DATABASE_SETTING['password'], DATABASE_SETTING['host'])

    conn = create_engine(test_engine).connect()
    conn.execute('commit')
    str_db_exist = "select `table_schema` from `information_schema`.`tables` where `table_schema`='valor_test';"
    if conn.execute(str_db_exist).rowcount == 0:
        conn.execute('create database `valor_test`;')
        conn.close()
    '''
    from base import engine
    metadata.create_all(engine)
    conn = engine.connect()
    conn.execute(site_model.insert(), mods)
