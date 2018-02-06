
#coding:utf8

from app import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from flask_moment import datetime
from markdown import markdown
import bleach
from mdx_gfm import GithubFlavoredMarkdownExtension
class Permission:
    FOLLOW = 0x01
    COMMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')  # create a role in User

    def __repr__(self):
        return 'Role %r' % self.name

    @staticmethod
    def insert_role():  # this be used to update role
        roles = {'User': (Permission.FOLLOW |
                          Permission.COMMMENT |
                          Permission.WRITE_ARTICLES, True),
                 'Moderator': (Permission.FOLLOW |
                               Permission.COMMMENT |
                               Permission.WRITE_ARTICLES |
                               Permission.MODERATE_COMMENTS, False),
                 'Administrator': (0xff, False)

                 }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(self.id)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def confirm(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def password_setter(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def generate_fake(self,f,t):#生成从f到t的用户
        for i in range (f,t):
            user = User(name=str(i),password='123',email=str(i),confirmed=True)
            db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return 'User %r' % self.name

class AnonymousUser(AnonymousUserMixin):
    def can(self, Permission):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    title = db.Column(db.String(64))
    type = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 相当于在post里有一个.user可以直接拿到User
    body_html = db.Column(db.Text)
    comments = db.relationship('Comment', backref='comments', lazy='dynamic')

    @staticmethod
    def generate_fake(num):
        for i in range(0, num):
            post=Post(body=str(num),author_id=1)
            db.session.add(post)
        db.session.commit()

    @staticmethod
    def on_change_body(target,value,oldvalue,initiator):
        # allowed_tags = ['a','abbr','acronym','b','blockquote','code','em','i','li','ol','pre','strong'
        #                 ,'ul','h1','h2','h3','p','img']
        target.body_html = markdown(value, output_format='html', extensions=[GithubFlavoredMarkdownExtension()])
db.event.listen(Post.body,'set',Post.on_change_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 相当于在post里有一个.user可以直接拿到User
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    body_html = db.Column(db.Text)
    @staticmethod
    def on_change_body(target,value,oldvalue,initiator):
        allowed_tags = ['a','abbr','acronym','b','blockquote','code','em','i', 'li','ol','pre','strong'
                        ,'ul','h1','h2','h3','p','img']
        target.body_html = bleach.linkify(bleach.clean(markdown(value,output_format='html'),tags=allowed_tags,strip=True))

#db.event.listen(Comment.body,'set',Comment.on_change_body)


class TodoList(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
