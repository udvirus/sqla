#!/usr/bin/python
# coding: utf-8
from sqlalchemy import Table, Column, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR, BOOLEAN, TEXT, DECIMAL

metadata    = MetaData()

user_base = Table('user_base', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
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
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_profile = Table('user_profile', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('thumb_id', INTEGER(unsigned=True), ForeignKey('user_image.id')),    # User Image ID
    Column('nickname', VARCHAR(16)),    # User Nickname
    Column('gender', TINYINT(unsigned=True), nullable=False, default=2),    # Gender
    Column('_birthday', INTEGER(unsigned=True)), 
    Column('first_name', VARCHAR(32)) ,
    Column('last_name', VARCHAR(32)),
    Column('cellphone', VARCHAR(16)),
    Column('country', VARCHAR(256)),
    Column('province', VARCHAR(256)),
    Column('city', VARCHAR(256)),
    Column('address', VARCHAR(256)), 
    Column('website', VARCHAR(256)),
    Column('excerpt', VARCHAR(256)),    # short intro
    Column('intro', TEXT),       # long intro

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_relation = Table('user_relation', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('target_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('reverse', BOOLEAN, nullable=False, default=True),   # user_id is followed
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('user_id', 'target_id', 'reverse'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_friendtag = Table('user_friendtag', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('name', VARCHAR(32), nullable=False, index=True),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_friendsgroup = Table('user_friendsgroup', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('target_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('friendtag_id', INTEGER(unsigned=True), ForeignKey('user_friendtag.id'), nullable=False),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('user_id', 'target_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_mail = Table('user_mail', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),  # People who get mail
    Column('message_id', INTEGER(unsigned=True), ForeignKey('user_message.id'), nullable=False),
    Column('read', BOOLEAN, nullable=False, default=0),
    Column('delete', BOOLEAN, nullable=False, default=0),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('user_id', 'message_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_message = Table('user_message', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('init', BOOLEAN, nullable=False, default=0),
    Column('draft', BOOLEAN, nullable=False, default=0),

    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('headline', VARCHAR(256), nullable=False),
    Column('content', TEXT),

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_album = Table('user_album', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('headline', VARCHAR(256), nullable=False),
    Column('intro', TEXT),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_image = Table('user_image', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('icon', BOOLEAN, nullable=False, default=0),          # icon or picture

    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('servname', VARCHAR(32), nullable=False, unique=True),   # filename without suffix
    Column('filetype', VARCHAR(8), nullable=False),                 # filetype as suffix
    Column('basename', VARCHAR(64), nullable=False),                # file native name
    Column('filesize', INTEGER(unsigned=True)),                     # capacity
    Column('width', INTEGER(unsigned=True)),                        # width
    Column('height', INTEGER(unsigned=True)),                       # height

    Column('like', TEXT),                                           # list of people who likes

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_album_image = Table('user_album_image', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('album_id', INTEGER(unsigned=True), ForeignKey('user_album.id'), nullable=False),
    Column('image_id', INTEGER(unsigned=True), ForeignKey('user_image.id'), nullable=False),
    Column('alias', VARCHAR(32)),
    Column('intro', TEXT),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('album_id', 'image_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

user_event = Table('user_event', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('object_type_id', TINYINT(unsigned=True), nullable=False),
    Column('object_pk', INTEGER(unsigned=True), nullable=False),
    Column('hide', BOOLEAN, nullable=False, default=0),
    Column('message', TEXT),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

news_category = Table('news_category', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('name', VARCHAR(16), nullable=False, unique=True),
    Column('segment', VARCHAR(128), nullable=False, unique=True), 
    Column('sort', INTEGER, nullable=False, default=0),
    Column('summary', VARCHAR(512)),
    Column('intro', TEXT),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

news_detail = Table('news_detail', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('init', BOOLEAN, nullable=False, default=0),
    Column('enable_publish', BOOLEAN, nullable=False, default=0),

    Column('category_id', INTEGER(unsigned=True), ForeignKey('news_category.id'), nullable=False),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),

    Column('headline', VARCHAR(256)),
    Column('thumb_id', INTEGER(unsigned=True), ForeignKey('user_image.id')),
    Column('summary', VARCHAR(512)),

    Column('enable_anonymous', BOOLEAN, nullable=False, default=0),
    Column('enable_comment', BOOLEAN, nullable=False, default=1),

    Column('count_visit', INTEGER(unsigned=True), nullable=False, default=0),
    Column('count_comment', INTEGER(unsigned=True), nullable=False, default=0),
    Column('count_like', INTEGER(unsigned=True), nullable=False, default=0),

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

news_content = Table('news_content', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('news_id', INTEGER(unsigned=True), ForeignKey('news_detail.id'), nullable=False),
    Column('content', TEXT),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_taxonomy = Table('game_taxonomy', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('is_genre', BOOLEAN, nullable=False, default=0),
    Column('name', VARCHAR(32), nullable=False),
    Column('segment', VARCHAR(128), nullable=False), 
    Column('sort', INTEGER, nullable=False, default=0),
    Column('alias', VARCHAR(64)),
    Column('summary', VARCHAR(512)),
    Column('intro', TEXT),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('is_genre', 'segment'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_detail = Table('game_detail', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('init', BOOLEAN, nullable=False, default=0),
    Column('enable_publish', BOOLEAN, nullable=False, default=0),

    Column('genre_id', INTEGER(unsigned=True), ForeignKey('game_taxonomy.id'), nullable=False),
    Column('headline', VARCHAR(256), nullable=False),
    Column('thumb_id', INTEGER(unsigned=True), ForeignKey('user_image.id')),
    Column('alias', VARCHAR(256)),
    Column('developer', VARCHAR(256)),
    Column('developer_site', VARCHAR(128)),
    Column('publisher', VARCHAR(256)),
    Column('publisher_site', VARCHAR(128)),
    Column('release_date', INTEGER(unsigned=True), nullable=False, default=0),

    Column('summary', VARCHAR(512)),

    Column('count_score', INTEGER(unsigned=True), nullable=False, default=0),
    Column('count_critic', INTEGER(unsigned=True), nullable=False, default=0),
    Column('count_mark', INTEGER(unsigned=True), nullable=False, default=0),
    Column('count_like', INTEGER(unsigned=True), nullable=False, default=0),
    Column('count_play', INTEGER(unsigned=True), nullable=False, default=0),

    Column('count_visit', INTEGER(unsigned=True), nullable=False, default=0),
    Column('count_comment', INTEGER(unsigned=True), nullable=False, default=0),

    Column('total_score', INTEGER(unsigned=True), nullable=False, default=0),
    Column('total_graph', INTEGER(unsigned=True), nullable=False, default=0),
    Column('total_control', INTEGER(unsigned=True), nullable=False, default=0),
    Column('total_opera', INTEGER(unsigned=True), nullable=False, default=0),
    Column('total_music', INTEGER(unsigned=True), nullable=False, default=0),

    Column('latest_version', VARCHAR(32)),

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_content = Table('game_content', metadata, 
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),
    Column('content', TEXT),
    Column('change_log', TEXT),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_genre = Table('game_genre', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),
    Column('genre_id', INTEGER(unsigned=True), ForeignKey('game_taxonomy.id'), nullable=False),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('game_id', 'genre_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_platform = Table('game_platform', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),
    Column('platform_id', INTEGER(unsigned=True), ForeignKey('game_taxonomy.id'), nullable=False),
    Column('price_cny', DECIMAL(precision=8, scale=2), nullable=False, default=0),
    Column('price_usd', DECIMAL(precision=8, scale=2), nullable=False, default=0),
    Column('discount', TINYINT(unsigned=True), nullable=False, index=True, default=100),
    Column('capacity', INTEGER(unsigned=True)),     # Game Capacity(M)
    Column('current_version', VARCHAR(32)),         # Current Platform Game Version(maybe not lastest version)
    Column('system_version', VARCHAR(1024)),        # System Version Require
    Column('language', VARCHAR(512)),               # Language Support
    Column('download_site', VARCHAR(128)),          # Market Download Addr
    Column('_upgrade', INTEGER(unsigned=True)),     # UNIX TIMESTAMP
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('platform_id', 'game_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_review = Table('game_review', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('init', BOOLEAN, nullable=False, default=0),

    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),

    Column('count_visit', INTEGER(unsigned=True), nullable=False, default=0),
    Column('count_comment', INTEGER(unsigned=True), nullable=False, default=0), 

    Column('graph', TINYINT(unsigned=True), nullable=False, default=0),
    Column('control', TINYINT(unsigned=True), nullable=False, default=0),
    Column('opera', TINYINT(unsigned=True), nullable=False, default=0),
    Column('music', TINYINT(unsigned=True), nullable=False, default=0),

    # List of people id, e.p: 1,2,3...
    Column('agree', TEXT),
    Column('disagree', TEXT),

    Column('headline', VARCHAR(256)),
    Column('content', TEXT),

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('user_id', 'game_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_mark = Table('game_evaluation', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),

    Column('mark', INTEGER(unsigned=True), nullable=False, default=0),      # 0=>unmark, unix_timestamp=>mark
    Column('play', INTEGER(unsigned=True), nullable=False, default=0),      # 0=>unplay, unix_timestamp=>play
    Column('like', INTEGER(unsigned=True), nullable=False, default=0),      # 0=>unlike, unix_timestamp=>like

    Column('scored', INTEGER(unsigned=True), nullable=False, default=0),    # 0=>unscore, unix_timestamp=>score
    Column('score', TINYINT(unsigned=True), nullable=False, default=0),

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('user_id', 'game_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_guide = Table('game_guide', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('init', BOOLEAN, nullable=False, default=0),

    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),

    Column('headline', VARCHAR(256)),
    Column('summary', VARCHAR(512)),
    Column('content', TEXT),

    Column('agree', TEXT),
    Column('disagree', TEXT),

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

game_image = Table('game_image', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('gallery', BOOLEAN, nullable=False, default=0),

    Column('game_id', INTEGER(unsigned=True), ForeignKey('game_detail.id'), nullable=False),
    Column('image_id', INTEGER(unsigned=True), ForeignKey('user_image.id'), nullable=False),

    Column('gallery_sort', TINYINT, nullable=False, default=0),
    Column('gallery_headline', VARCHAR(256)),
    Column('gallery_summary', VARCHAR(512)),

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_apply = Table('group_apply', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), nullable=False),
    Column('actived', BOOLEAN, nullable=False, default=0),
    Column('active_code', VARCHAR(32), nullable=False),
    Column('deal', BOOLEAN, nullable=False, default=0),
    Column('privacy', BOOLEAN, nullable=False, default=0),
    Column('headline', VARCHAR(256), nullable=False),
    Column('remark', VARCHAR(512)),
    Column('intro', TEXT),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_detail = Table('group_detail', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('headline', VARCHAR(256), nullable=False, unique=True),
    Column('thumb_id', INTEGER(unsigned=True), ForeignKey('user_image.id')),

    Column('count_topic', INTEGER(unsigned=True), nullable=False, default=0),
    Column('count_member', INTEGER(unsigned=True), nullable=False, default=0),

    Column('enable_applicant_create_topic', BOOLEAN, nullable=False, default=1),
    Column('enable_people_create_topic', BOOLEAN, nullable=False, default=1),
    Column('enable_applicant_reply', BOOLEAN, nullable=False, default=1),
    Column('enable_people_reply', BOOLEAN, nullable=False, default=1),

    Column('summary', VARCHAR(512)),
    Column('intro', TEXT),

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_member = Table('group_member', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('group_id', INTEGER(unsigned=True), ForeignKey('group_detail.id'), nullable=False),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('roles', TINYINT(unsigned=True), nullable=False, default=2),     # 0=>founder, 1=>assistant, 2=>member, 3=>applicant
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('group_id', 'user_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_topic = Table('group_topic', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('init', BOOLEAN, nullable=False, default=0),
    Column('hide', BOOLEAN, nullable=False, default=0),

    Column('group_id', INTEGER(unsigned=True), ForeignKey('group_detail.id'), nullable=False),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),

    Column('enable_top', BOOLEAN, nullable=False, default=0),
    Column('top_sort', TINYINT, nullable=False, default=0),

    Column('count_reply', INTEGER(unsigned=True), nullable=False, default=0),
    Column('count_visit', INTEGER(unsigned=True), nullable=False, default=0),

    Column('recently_reply', INTEGER(unsigned=True), nullable=False),   # unix_timestamp, default = created
    Column('headline', VARCHAR(256)),

    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

group_reply = Table('group_reply', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('topic_id', INTEGER(unsigned=True), ForeignKey('group_topic.id'), nullable=False),
    Column('hide', BOOLEAN, nullable=False, default=0),
    Column('is_reply', BOOLEAN, nullable=False, default=0),
    Column('content', TEXT),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

tag_content = Table('tag_content', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('content', VARCHAR(32), nullable=False, unique=True),
    Column('references', INTEGER(unique=True), default=0),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

tag_mark = Table('tag_mark', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_base.id'), nullable=False),
    Column('object_type_id', INTEGER(unsigned=True), ForeignKey('site_model.id'), nullable=False),
    Column('object_pk', INTEGER(unsigned=True), nullable=False),
    Column('tag_id', INTEGER(unsigned=True), ForeignKey('tag_content.id'), nullable=False),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('user_id', 'object_type_id', 'object_pk', 'tag_id'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

site_model = Table('site_model', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('app_label', VARCHAR(64), nullable=False),
    Column('model', VARCHAR(64), nullable=False),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    UniqueConstraint('app_label', 'model'),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

site_seo = Table('site_seo', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('object_type_id', INTEGER(unsigned=True), ForeignKey('site_model.id'), nullable=False),
    Column('object_pk', INTEGER(unsigned=True), nullable=False),
    Column('page_title', VARCHAR(64)),
    Column('page_keyword', VARCHAR(128)),
    Column('page_description', VARCHAR(1024)),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
    mysql_engine        = 'InnoDB',
    mysql_charset       = 'utf8',
)

site_comment = Table('site_comment', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True),
    Column('user_id', INTEGER(unsigned=True), ForeignKey('user_profile.user_id')),
    Column('hide', BOOLEAN, nullable=False, default=0),
    Column('object_type_id', INTEGER(unsigned=True), ForeignKey('site_model.id'), nullable=False),
    Column('object_pk', INTEGER(unsigned=True), nullable=False),
    Column('username', VARCHAR(32)),
    Column('nickname', VARCHAR(64)),
    Column('email', VARCHAR(128)),
    Column('ipaddr', INTEGER(unsigned=True)),
    Column('user_thumb', VARCHAR(64)), # 64
    Column('content', TEXT),
    Column('_created', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp()),
    Column('_modified', INTEGER(unsigned=True), nullable=False, default=func.unix_timestamp(), onupdate=func.unix_timestamp()),
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
