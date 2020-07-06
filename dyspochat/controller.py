import hashlib
import time

from random import randint

from .model import *
from . import db


def get_user_all():
    with db.session() as sess:
        return [i for i in sess.query(User).all()]

def get_user_username(username: str):
    with db.session() as sess:
        for i in sess.query(User).all():
            if username == i.username:
                return  i

def get_user_id(user_id: int):
    with db.session() as sess:
        for i in sess.query(User).all():
            if int(user_id) == int(i.id):
                return i

def add_user(username, password):
    for i in get_user_all():
        if i.username == username:
            return (False, "username_exist")

    with db.session() as sess:
        try:
            user = User(username=username, password=password)
            sess.add(user)
            return (True, get_user_username(user.username))
        except Exception as e:
            return (False, "server_error")
        

# Chat
def get_recipient_user(user):
    with db.session() as sess:
        for i in sess.query(ChatRecipient).all():
            if(i.user_id == user.id):
                return i

def add_recipient(chatroom, user):
    with db.session() as sess:
        recipients = ChatRecipient(chatroom=chatroom, user=user)
        try:
            sess.add(recipients)
            return (True, get_recipient_user(user))
        except Exception as e:
            return (False, "server_error")
        
def get_chatroom_id(chatroom_id):
    with db.session() as sess:
        for i in sess.query(Chatroom).all():
            if int(chatroom_id) == int(i.id):
                return i

def get_chatroom_room_id(room_id):
    with db.session() as sess:
        for i in sess.query(Chatroom).all():
            if int(room_id) == int(i.room_id):
                return i

def create_chat(initial_recipient: User):
    with db.session() as sess:
        salt_data = str(time.time()) + "abcdefghijklmnopqrtuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[randint(0, 51)] + str(randint(0, 10000000))
        room_id = "".join([hashlib.md5((initial_recipient.username + initial_recipient.password + salt_data).encode("utf-8")).hexdigest()[i] for i in range(44)])

        chatroom = Chatroom(room_id)
        try:
            sess.add(chatroom)
            chatroom = get_chatroom_room_id(room_id)
            recipients = add_recipient(chatroom, initial_recipient)
            return (True, (chatroom, recipients[1]))
        except Exception as e:
            return (False, "server_error")

def get_messages():
    with db.session() as sess:
        return [i for i in sess.query(Message).all()]

def get_message(user, chatroom):
    with db.session() as sess:
        messages = []
        for i in sess.query(Message).all():
            if i.user_id == user.id and i.chatroom_id == chatroom.id:
                messages.append(i)
        
        return messages

def add_message(user: User, chatroom: Chatroom, content: str):
    with db.session() as sess:
        message = Message(user=user, chatroom=chatroom, content=str(content))

        try:
            sess.add(message)
            return True
        except Exception as e:
            return False
            