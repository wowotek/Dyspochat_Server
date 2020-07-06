import hashlib
import time

from random import randint

from .model import *
from . import db


def get_user_all():
    return [i for i in User.query.all()]

def get_user_username(username: str):
    for i in User.query.all():
        if username == i.username:
            return  i

def get_user_id(user_id: int):
    for i in User.query.all():
        if int(user_id) == int(i.id):
            return i

def add_user(username, password):
    for i in get_user_all():
        if i.username == username:
            return (False, "username_exist")

    try:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return (True, get_user_username(user.username))
    except Exception as e:
        return (False, "server_error")
        

# Chat
def get_recipient_user(user):
    for i in ChatRecipient.query.all():
        if(i.user_id == user.id):
            return i

def add_recipient(chatroom, user):
    recipients = ChatRecipient(chatroom=chatroom, user=user)
    try:
        db.session.add(recipients)
        db.session.commit()
        return (True, get_recipient_user(user))
    except Exception as e:
        return (False, "server_error")
        
def get_chatroom_id(chatroom_id):
    for i in Chatroom.query.all():
        if int(chatroom_id) == int(i.id):
            return i

def get_chatroom_room_id(room_id):
    for i in Chatroom.query.all():
        if int(room_id) == int(i.room_id):
            return i

def create_chat(initial_recipient: User):
    salt_data = str(time.time()) + "abcdefghijklmnopqrtuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[randint(0, 51)] + str(randint(0, 10000000))
    room_id = hashlib.md5((initial_recipient.username + initial_recipient.password + salt_data).encode("utf-8")).hexdigest()

    chatroom = Chatroom(room_id=room_id)
    try:
        db.session.add(chatroom)
        db.session.commit()
        chatroom = get_chatroom_room_id(room_id)
        recipients = add_recipient(chatroom, initial_recipient)
        return (True, (chatroom, recipients[1]))
    except Exception as e:
        print(e)
        return (False, e)

def get_messages():
    return [i for i in Message.query.all()]

def get_message(user, chatroom):
    messages = []
    for i in Message.query.all():
        if i.user_id == user.id and i.chatroom_id == chatroom.id:
            messages.append(i)
    
    return messages

def add_message(user: User, chatroom: Chatroom, content: str):
    message = Message(user=user, chatroom=chatroom, content=str(content))

    try:
        db.session.add(message)
        db.session.commit()
        return True
    except Exception as e:
        return False
        