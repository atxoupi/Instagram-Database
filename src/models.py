import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy import render_er

Base = declarative_base()

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    userName = Column(String(250))
    firtsName = Column(String(250))
    lastName = Column(String(250))
    email = Column(String(250), nullable=False)
    user_from = relationship('follower', backref='user', lazy=True)
    user_to = relationship('follower', backref='user', lazy=True)
    user_comment = relationship('comment', backref='user', lazy=True)
    user_post = relationship('post', backref='user', lazy=True)
    followers = relationship('follow_user', secondary=follow_user, lazy='subquery',
        backref=backref('user', lazy=True))

follow_user = Table('follow_user',
    Column('follower_id', Integer, db.ForeignKey('follower.id'), primary_key=True),
    Column('user_id', Integer, db.ForeignKey('user.id'), primary_key=True)
)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    commentText = Column(String(250))
    autor_id = Column(Integer, ForeignKey('user.id'),nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'),nullable=False)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'),nullable=False)
    post_comment = relationship('comment', backref='post', lazy=True)
    post_media = relationship('media', backref='post', lazy=True)

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(String(25))
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'),nullable=False)

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e