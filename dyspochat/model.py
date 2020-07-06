# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from . import db


class ChatRecipient(db.Model):
    __tablename__ = 'chat_recipients'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    chatroom_id = db.Column(db.ForeignKey('chatroom.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, unique=True)

    chatroom = db.relationship('Chatroom', primaryjoin='ChatRecipient.chatroom_id == Chatroom.id', backref='chat_recipients')
    user = db.relationship('User', primaryjoin='ChatRecipient.user_id == User.id', backref='chat_recipients')



class Chatroom(db.Model):
    __tablename__ = 'chatroom'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    room_id = db.Column(db.String(45), nullable=False, unique=True)



class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, unique=True)
    chatroom_id = db.Column(db.ForeignKey('chatroom.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, unique=True)
    content = db.Column(db.Text)

    chatroom = db.relationship('Chatroom', primaryjoin='Message.chatroom_id == Chatroom.id', backref='messages')
    user = db.relationship('User', primaryjoin='Message.user_id == User.id', backref='messages')



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)