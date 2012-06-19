#!/usr/bin/python
# coding: utf-8
from sqlalchemy import or_,\
                       and_,\
                       select
from sqlalchemy.orm import mapper,\
                           relationship,\
                           object_session,\
                           deferred,\
                           outerjoin
from sqlalchemy.ext.hybrid import hybrid_property
from mako.template import Template

from .schema import *
from core.common import ascii_convert_unicode as _u
from core.func import int2datetime, datetime2int, ip2num, num2ip
from core.hash import random_string, random_token, hash_password


class BaseModel(object):
    _object_type_id     = None

    def __init__(self, *a, **kw):
        [hasattr(self, k) and setattr(self, k, v) for k, v in kw.iteritems()]

    @hybrid_property
    def modified(self):
        return int2datetime(self._modified)

    @modified.setter
    def modified(self, datetime):
        self._modified = datetime2int(datetime)

    @hybrid_property
    def created(self):
        return int2datetime(self._created)

    @created.setter
    def created(self, datetime):
        self._created = datetime2int(datetime)

    @hybrid_property
    def object_type_id(self):
        if self._object_type_id is None:
            app_label, model = self.__table_name__.split('_', 1)
            obj = object_session(self).query(SiteModel)\
                .filter(and_(
                    SiteModel.app_label     == app_label,
                    SiteModel.model         == model,
                )).first()
            self._object_type_id = obj.id if obj else None
        return self._object_type_id

    def update_by_form(self, formobj, deny=[]):
        deny.extend(['csrf', 'method'])
        map(
            lambda key: hasattr(self, key) and setattr(self, key, formobj.data[key]),
            list(set(formobj.data.keys()).difference(deny)),
        )

class AbstractTagModel(object):
    def get_user_tags(self, uid, quantity=10):
        return object_session(self).query(TagMark, TagContent)\
            .select_from(
                outerjoin(TagMark, TagContent, TagMark.tag_id==TagContent.id),
            ).filter(and_(
                TagMark.object_type_id      == self.object_type_id,
                TagMark.object_pk           == self.id,
                TagMark.user_id             == uid,
            ))[0:quantity]

    def update_user_tags(self, uid, tags=[], quantity=10):
        old_tags = map(
            lambda obj: obj[1].content,
            self.get_user_tags(uid, quantity=quantity),
        )

        removes = list(set(old_tags).difference(tags))
        adds    = list(set(tags).difference(old_tags))

        ''' remove tags '''
        if removes:
            remove_tags = object_session(self).query(TagMark, TagContent)\
                .select_from(
                    outerjoin(TagMark, TagContent, TagMark.tag_id==TagContent.id),
                ).filter(and_(
                    TagMark.object_type_id  == self.object_type_id,
                    TagMark.object_pk       == self.id,
                    TagMark.user_id         == uid,
                    TagContent.content.in_(removes),
                )).all()

            for tm, tc in remove_tags:
                object_session(self).delete(tm)
                tc.minus_references()

        ''' add tags '''
        if adds:
            for tag in adds:
                tm = TagMark(
                    object_type_id  = self.object_type_id,
                    object_pk       = self.id,
                    user_id         = uid,
                )
                tm.mark_tag(object_session(self), tag)
                object_session(self).add(tm)

    def tags(self, uid, quantity=10):
        return ' '.join(map(
            lambda obj: obj[1].content,
            self.get_user_tags(uid, quantity),
        ))

class UserBase(BaseModel): 
    __table_name__ = user_base.name

    @hybrid_property
    def login_addr(self):
        return num2ip(self._login_addr)

    @login_addr.setter
    def login_addr(self, ip_addr):
        self._login_addr = ip2num(ip_addr)

    @hybrid_property
    def last_login(self):
        return int2datetime(self._last_login)

    @last_login.setter
    def last_login(self, datetime):
        self._last_login = datetime2int(datetime)

    def _set_password(self, password):
        self.secret = random_string()
        self.login_sequence = random_token()
        self.password = hash_password(_u(password), self.secret)

    def create_user(self, email, username, password, ipaddr):
        self.secret = random_string()
        self.email = email
        self.username = username
        self._set_password(password)
        self.login_addr = ipaddr
        self.active_token = random_token()
        self.user_profile = UserProfile()

    def create_admin(self):
        self.admin = 1

    def create_root(self):
        self.admin, self.root = 1, 1

    def reset_password(self, old, new):
        if self.password == hash_password(old, self.secret):
            self._set_password(new)
            msg = repr((u'更新了密码.', {}))
            create_object_type(object_session(self), UserEvent, self, self.id,\
                user_id=self.id, message=msg,
            )

    def attention_to(self, people_id):
        ''' 是否跟随了某人
        '''
        pass

    def followed_by(self, people_id):
        ''' 是否被某人跟随了
        '''
        pass

    def get_friendtags(self, start=0, offset=10):
        return object_session(self).query(UserFriendtag)\
            .filter(UserFriendtag.user_id==self.id)[start:offset]

    def init_session(self):
        return dict(id=self.id, email=self.email, username=self.username,\
            gender=self.user_profile.gender, thumb=self.user_profile.thumb,\
            last_name=self.user_profile.last_name, first_name=self.user_profile.first_name,\
            fullname=self.user_profile.fullname, nickname=self.user_profile.nickname,\
            created=self.created, last_login=self.last_login, admin=self.admin, root=self.root,\
            login_addr=self.login_addr, login_sequence=self.login_sequence, login_token=self.login_token,\
            _last_login=self._last_login, modified=self.modified, _modified=self._modified,\
        )

class UserProfile(BaseModel): 
    __table_name__ = user_profile.name

    @hybrid_property
    def fullname(self):
        if self.last_name is None or self.first_name is None:
            return None
        return '%s %s' % (self.last_name, self.first_name)

    @hybrid_property
    def birthday(self):
        return int2datetime(self._birthday)

    @birthday.setter
    def birthday(self, datetime):
        self._birthday = datetime2int(datetime)

    @hybrid_property
    def t_nickname(self):
        return self.nickname\
            if self.nickname and len(self.nickname) > 0\
            else self.username

class UserRelation(BaseModel): 
    __table_name__ = user_relation.name 

class UserFriendtag(BaseModel): 
    __table_name__ = user_friendtag.name

class UserFriendsgroup(BaseModel): 
    __table_name__ = user_friendsgroup.name

class UserMail(BaseModel):
    __table_name__ = user_mail.name

class UserMessage(BaseModel):
    __table_name__ = user_message.name

class UserAlbum(BaseModel): 
    __table_name__ = user_album.name

class UserImage(BaseModel): 
    __table_name__ = user_image.name

class UserGallery(BaseModel):
    __table_name__ = user_gallery.name

class UserEvent(BaseModel):
    ''' message: (str, dict)
    '''
    __table_name__ = user_event.name

    @hybrid_property
    def format_message(self):
        try:
            msg, params = eval(self.message)
            if isinstance(msg, (str, unicode)) and isinstance(params, dict):
                return Template(msg).render(**params)
        except:
            return None

    def set_message(self, msg, **kw):
        self.message = repr((msg, kw))


class NewsCategory(BaseModel): 
    __table_name__ = news_category.name

class NewsDetail(BaseModel): 
    __table_name__ = news_detail.name

    def get_comments(self, start=0, offset=10):
        return object_session(self).query(SiteComment)\
            .filter(and_(
                SiteComment.object_type_id  == self.object_type_id,
                SiteComment.object_pk       == self.id,
                SiteComment.show            == 1,
            )).order_by(SiteComment._created.desc())[start:offset]

class NewsContent(BaseModel): 
    __table_name__ = news_content.name


class GameTaxonomy(BaseModel):
    __table_name__ = game_taxonomy.name

class GameDetail(AbstractTagModel, BaseModel): 
    __table_name__ = game_detail.name

class GameContent(BaseModel): 
    __table_name__ = game_content.name

# relation ship 
class GameGenre(BaseModel):
    __table_name__ = game_genre.name

class GamePlatform(BaseModel): 
    __table_name__ = game_platform.name

class GameReview(BaseModel):
    __table_name__ = game_review.name

class GameMark(BaseModel): 
    __table_name__ = game_mark.name

class GameGuide(BaseModel):
    __table_name__ = game_guide.name

class GameImage(BaseModel):
    __table_name__ = game_image.name


class GroupApply(BaseModel):
    __table_name__ = group_apply.name

class GroupDetail(BaseModel):
    __table_name__ = group_detail.name

class GroupMember(BaseModel):
    __table_name__ = group_member.name

class GroupTopic(BaseModel):
    __table_name__ = group_topic.name

class GroupReply(BaseModel):
    __table_name__ = group_reply.name


class TagContent(BaseModel):
    __table_name__ = tag_content.name 

    def add_references(self, add=1):
        self.references = self.references + add

    def minus_references(self, minus=1):
        self.references = self.references - 1 if self.references > 0 else 0

class TagMark(BaseModel):
    __table_name__ = tag_mark.name

    def mark_tag(self, db, tag):
        tc = db.query(TagContent)\
            .filter(TagContent.content==tag).first()

        if tc:
            tc.add_references()
            self.tag_id         = tc.id
        else:
            self.tag_content    = TagContent(content=tag, references=0)
            self.tag_content.add_references()
        return self

    def unmark_tag(self):
        self.tag_content.minus_references()
        return self

class SiteSeo(BaseModel):
    __table_name__ = site_seo.name

class SiteModel(BaseModel):
    __table_name__ = site_model.name

    @hybrid_property
    def object_name(self):
        fmt_model = map(lambda s: s.capitalize(), self.model.split('_'))
        return self.app_label.capitalize() + ''.join(fmt_model)

    @hybrid_property
    def table_name(self):
        return '%s_%s' % (self.app_label, self.model)

class SiteComment(BaseModel):
    __table_name__ = site_comment.name

mapper(UserBase, user_base, properties={
    'user_profile': relationship(UserProfile, uselist=False, backref='user_base'),
    'user_albums': relationship(UserAlbum, backref='user_base', order_by=user_album.c.id),
    'user_events': relationship(UserEvent, backref='user_base', order_by=user_event.c._created.desc()),
    'user_friendtags': relationship(UserFriendtag, backref='user_base', order_by=user_friendtag.c.id),
    'user_relations': relationship(UserRelation, 
        primaryjoin=user_base.c.id==user_relation.c.user_id,
        backref='user_base', 
        order_by=user_relation.c._created.desc(),
    ),
})

mapper(UserProfile, user_profile, properties={
    'news_details': relationship(NewsDetail, 
        backref='user_profile', order_by=news_detail.c.id,
    ),
    'user_friendtags': relationship(UserFriendtag,
        secondary=user_friendsgroup, backref='user_profile',
    ),
    'username': deferred(
        select([user_base.c.username]).where(user_base.c.id==user_profile.c.user_id),
    ),
    'comments': relationship(SiteComment, 
        backref='user_profile', order_by=site_comment.c._created.desc(),
    ),
})
mapper(UserRelation, user_relation)
mapper(UserFriendtag, user_friendtag, properties={
    'group_friends': relationship(UserProfile,
        secondary=user_friendsgroup, backref='user_friendtag',
    ),
})
mapper(UserFriendsgroup, user_friendsgroup)
mapper(UserMail, user_mail)
mapper(UserMessage, user_message)
mapper(UserAlbum, user_album)
mapper(UserImage, user_image)
mapper(UserGallery, user_gallery)
mapper(UserEvent, user_event)


mapper(NewsCategory, news_category, properties={
    'news_details': relationship(NewsDetail, 
        backref='news_category', order_by=news_detail.c.id,
    ),
})
mapper(NewsDetail, news_detail, properties={
    'news_content': relationship(NewsContent, 
        uselist=False, backref='news_detail',
    ),
    'category': deferred(
        select([news_category.c.name]).where(news_category.c.id==news_detail.c.category_id),
    ),
    'content': deferred(
        select([news_content.c.content]).where(news_content.c.news_id==news_detail.c.id),
    ),
})
mapper(NewsContent, news_content)


mapper(GameTaxonomy, game_taxonomy, properties={
    'game_details': relationship(GameDetail, 
        backref='game_taxonomy', order_by=game_detail.c.id,
    ),
})

mapper(GamePlatform, game_platform)

mapper(GameContent, game_content)

mapper(GameDetail, game_detail, properties={
    'game_content': relationship(GameContent, 
        uselist=False, backref='game_detail',
    ),
    'game_marks': relationship(GameMark,
        backref='game_detail', order_by=game_mark.c.id,
    ),
    'genre': deferred(
        select([game_taxonomy.c.name]).where(game_taxonomy.c.id==game_detail.c.genre_id),
    ),
    'content': deferred(
        select([game_content.c.content]).where(game_content.c.game_id==game_detail.c.id),
    ),
})

mapper(GameMark, game_mark)

mapper(GroupDetail, group_detail)


mapper(TagContent, tag_content, properties={
    'tag_marks': relationship(TagMark,
        backref='tag_content', order_by=tag_mark.c.id,
    ),
})
mapper(TagMark, tag_mark)

mapper(SiteSeo, site_seo)
mapper(SiteComment, site_comment)
mapper(SiteModel, site_model)

def create_object_type(db, ct_obj, obj, pk, *a, **kw):
    app_label, model = obj.__table_name__.split('_', 1)
    object_type_id = db.query(SiteModel)\
        .filter(and_(
            SiteModel.app_label==app_label,
            SiteModel.model==model,
        )).first().id
    kw.update(dict(
        object_type_id=object_type_id, 
        object_pk=pk,
    ))
    db.add(ct_obj(**kw))

def get_object_type(db, ct_obj, obj, pk, **kw):
    ''' Return a query string object without fetch. '''
    app_label, model = obj.__table_name__.split('_', 1)
    object_type_id = db.query(SiteModel)\
        .filter(and_(
            SiteModel.app_label==app_label,
            SiteModel.model==model,
        )).first().id
    return db.query(ct_obj).filter(and_(
        ct_obj.object_type_id==object_type_id,
        ct_obj.object_pk==pk,
    )).filter_by(**kw).all()

def get_or_create(db, obj, **kw):
    instance = db.query(obj).filter_by(**kw).first()
    if instance:
        return instance, False
    else:
        instance = obj(**kw)
        return instance, True
