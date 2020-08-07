#!/usr/bin/python3
import time
from functools import wraps

from flask import jsonify, request, abort
from flask_json import json_response

from . import app, db, event_pusher
from .models import User, Chat, Chatroom, Session, SessionData
from .misc import generate_pseudonym


################# API-KEY DECORATOR #################
def require_apikey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == "wowotek-key":
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function
############### END API-KEY DECORATOR ###############

################# SESSION DECORATOR #################
def require_session(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-session-key'):
            for i in db.get_session_all():
                if request.headers.get('x-session-key') == i.session_hash:
                    return view_function(*args, **kwargs)
            abort(401)
        else:
            abort(401)
    return decorated_function
############### END SESSION DECORATOR ###############

################## MISC BLUEPRINTS ##################
@app.route('/misc/ping', methods=['GET'])
def ping():
    return json_response(
        status_=200,
        data_={
            "status": "success",
            "message": "pong!"
        }
    )

@app.route('/misc/hello', methods=['GET'])
@require_apikey
def apikey_check():
    return json_response(
        status_=200,
        data_={
            "status": "success",
            "message": "world"
        }
    )

@app.route('/misc/sane', methods=['GET'])
@require_apikey
def sanity_check():
    print("--- SANITY CHECK STARTED ---")
    sanity_data = db.add_sanity_check_data()

    if db.remove_sanity_check_data(sanity_data):
        print("SANITY CHECK ENDED")
        return json_response(
            status_=200,
            data_={
                "status": "success",
                "message": "i_am_sane",
                "sanity_data": sanity_data
            }
        )
    return json_response(
        status_=500,
        data_={
            "status": "failed",
            "message": "i am insane"
        }
    )

@app.route('/misc/pseudonym', methods=['GET'])
def get_pseudonym():
    return json_response(
        status_=200,
        data_={
            "status": "success",
            "pseudonym": generate_pseudonym()
        }
    )

################ END MISC BLUEPRINTS ################

################## USER BLUEPRINTS ##################
@app.route('/user/register', methods=['POST'])
@require_apikey
def user_register():
    username: str = str(request.json["username"])
    password: str = str(request.json["password"])

    add_status = db.add_user(User(username, password))
    if add_status[0]:
        print(f"user {add_status[1].username} registered")
        return json_response(
            status_=200,
            data_={
                "status": "success",
                "user": {
                    "id": add_status[1].id,
                    "username": add_status[1].username
                }
            }
        )

    return json_response(
        status_=200,
        data_={
            "status": "username_already_exist"
        }
    )


@app.route('/user/login', methods=['POST'])
@require_apikey
def user_login():
    username: str = str(request.json["username"])
    password: str = str(request.json["password"])

    user: User = db.get_user_username(username)
    if user != None:
        if user.password == password:
            session: Session = db.add_session()
            return json_response(
                status_=200,
                data_={
                    "status": "success",
                    "session": {
                        "id": session.id,
                        "key": session.session_hash
                    },
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "pseudonym": user.pseudonym
                    }
                }
            )
        return json_response(
            status_=200,
            data_={
                "status": "auth_failed"
            }
        )
    return json_response(
        status_=200,
        data_={
            "status": "user_not_found"
        }
    )

@app.route('/user/delete', methods=['POST'])
@require_apikey
def user_unregister():
    user_id: int = int(request.json["user_id"])
    status = db.del_user_id(user_id)

    if status[0]:
        return json_response(
            status_=200,
            data_={
                "status": "success",
                "user": {
                    "id": status[1].id,
                    "username": status[1].username,
                    "pseudonym": status[1].pseudonym
                }
            }
        )

    return json_response(
        status_=404,
        data_={
            "status": "user_not_found"
        }
    )

@app.route('/user/info', methods=['POST'])
@require_apikey
def user_info():
    user_id: int = int(request.json["user_id"])
    user: User = db.get_user_id(user_id)

    if user == None:
        return json_response(
            status_=404,
            data_={
                "status": "user_not_found"
            }
        )

    return json_response(
        status_=200,
        data_={
            "status": "success",
            "user": {
                "id": user.id,
                "username": user.username,
                "pseudonym": user.pseudonym
            }
        }
    )
################ END USER BLUEPRINTS ################

################ CHATROOM BLUEPRINTS ################
@app.route('/chatroom/add', methods=['POST'])
@require_apikey
def chatroom_add():
    chatroom: Chatroom = db.add_chatroom()
    if chatroom:
        print(f"{chatroom.id} created")
        return json_response(
            status_=200,
            data_={
                "status": "success",
                "chatroom": {
                    "id": chatroom.id
                }
            }
        )
    return json_response(
        status_=200,
        data_={
            "status": "chatroom_internal_server_error"
        }
    )

@app.route('/chatroom/info', methods=['POST'])
@require_apikey
def chatroom_info():
    chatroom_id: int = int(request.json["chatroom_id"])
    chatroom: Chatroom = db.get_chatroom(chatroom_id)

    if chatroom:
        return json_response(
            status_=200,
            data_={
                "status": "success",
                "chatroom": {
                    "id": chatroom.id,
                    "recipients": [
                        {
                            "id": i.id,
                            "username": i.username,
                            "pseudonym": i.pseudonym
                        } for i in chatroom.recipients
                    ],
                    "chats": [
                        {
                            "id": i.id,
                            "sender": {
                                "id": i.sender.id,
                                "username": i.sender.username,
                                "pseudonym": i.sender.pseudonym
                            },
                            "timestamp": i.timestamp,
                            "message": i.message
                        } for i in chatroom.chats
                    ]
                }
            }
        )
    return json_response(
        status_=404,
        data_={
            "status": "chatroom_not_found"
        }
    )

@app.route('/chatroom/delete', methods=['POST'])
@require_apikey
def chatroom_delete():
    chatroom_id: int = int(request.json["chatroom_id"])
    chatroom = db.delete_chatroom(chatroom_id)

    if chatroom:
        event_pusher.trigger(
            str(chatroom.id),
            u'del_chat',
            {
                "chatroom": {
                    "id": chatroom.id
                }
            }
        )
        return json_response(
            status_=200,
            data_={
                "status": "success",
                "chatroom": {
                    "id": chatroom.id
                }
            }
        )
    return json_response(
        status_=200,
        data_={
            "status": "chatroom_not_found"
        }
    )

@app.route('/chatroom/recipient/add', methods=['POST'])
@require_apikey
def chatroom_add_recipients():
    print("chatroom_add_recipients", request.json)
    chatroom_id = int(request.json["chatroom_id"])
    recipient_id = int(request.json["recipient_id"])

    chatroom: Chatroom = db.get_chatroom(chatroom_id)
    recipient: User = db.get_user_id(recipient_id)

    if chatroom:
        if recipient:
            add_join_party = True
            # check if recipient already exist
            # for i in chatroom.chats:
            #     if "joined the party" in i.message:
            #         add_join_party = False
        
            if add_join_party:
                chatroom.add_chat(
                    Chat(
                        db.get_chat_last_id(chatroom.id),
                        recipient,
                        time.time(),
                        f"{recipient.pseudonym} joined the party"
                    )
                )
            event_pusher.trigger(
                str(chatroom.id),
                u'new_recipient',
                {
                    "chatroom": {
                        "id": chatroom.id
                    },
                    "recipient": {
                        "id": recipient.id,
                        "username": recipient.username,
                        "pseudonym": recipient.pseudonym
                    }
                }
            )
            for i in chatroom.recipients:
                if i.id == recipient.id:
                    return json_response(
                        status_=200,
                        data_={
                            "status": "recipient_already_exist"
                        }
                    )
            chatroom.add_recipients(recipient)
            return json_response(
                status_=200,
                data_={
                    "status": "success"
                }
            )
        return json_response(
            status_=404,
            data_={
                "status": "recipient_not_found"
            }
        )
    return json_response(
        status_=404,
        data_={
            "status": "chatroom_not_found"
        }
    )


@app.route('/chatroom/recipient/delete', methods=['POST'])
@require_apikey
def chatroom_del_recipients():
    chatroom_id = int(request.json["chatroom_id"])
    recipient_id = int(request.json["recipient_id"])

    chatroom: Chatroom = db.get_chatroom(chatroom_id)
    recipient: User = db.get_user_id(recipient_id)

    if chatroom:
        if recipient:
            # check if recipient exist in chatroom
            for i in chatroom.recipients:
                if i.id == recipient.id:
                    add_leave_party = True
                    # for i in chatroom.chats:
                    #     if "is leaving chatroom" in i.message:
                    #         add_leave_party = False
                    if add_leave_party:
                        chatroom.add_chat(
                            Chat(
                                db.get_chat_last_id(chatroom.id),
                                recipient,
                                time.time(),
                                f"{recipient.pseudonym} is leaving chatroom"
                            )
                        )
                    chatroom.recipients.remove(i)
                    event_pusher.trigger(
                        str(chatroom.id),
                        u'del_recipient',
                        {
                            "chatroom": {
                                "id": chatroom.id
                            },
                            "recipient": {
                                "id": recipient.id,
                                "username": recipient.username,
                                "pseudonym": recipient.pseudonym
                            }
                        }
                    )
                    return json_response(
                        status_=200,
                        data_={
                            "status": "success",
                            "user": {
                                "id": recipient.id,
                                "pseudonym": recipient.pseudonym,
                                "username": recipient.username
                            }
                        }
                    )
            return json_response(
                status_=404,
                data_={
                    "status": "recipient_not_in_chatroom"
                }
            )
        return json_response(
            status_=404,
            data_={
                "status": "recipient_not_found"
            }
        )
    return json_response(
        status_=404,
        data_={
            "status": "chatroom_not_found"
        }
    )
############## END CHATROOM BLUEPRINTS ##############

################## CHAT BLUEPRINTS ##################
@app.route('/chat/add', methods=['POST'])
@require_apikey
def chat_add():
    chatroom_id = int(request.json["chatroom_id"])
    chat_sender = int(request.json["chat_sender"])
    chat_message = str(request.json["chat_message"])

    chatroom: Chatroom = db.get_chatroom(chatroom_id)
    chat_sender: User = db.get_user_id(chat_sender)

    if chatroom:
        if chat_sender:
            for i in chatroom.recipients:
                if i.id == chat_sender.id:
                    last_chat_id = db.get_chat_last_id(chatroom_id) + 1
                    chat: Chat = Chat(last_chat_id, chat_sender, time.time(), chat_message)
                    chatroom.add_chat(chat)
                    event_pusher.trigger(
                        str(chatroom.id),
                        u'new_chat',
                        {
                            "chatroom": {
                                "id": chatroom.id
                            },
                            "chat": {
                                "id": chat.id,
                                "timestamp": chat.timestamp,
                                "sender": {
                                    "id": chat.sender.id,
                                    "username": chat.sender.username,
                                    "pseudonym": chat.sender.pseudonym
                                },
                                "message": chat.message
                            }
                        }
                    )
                    return json_response(
                        status_=200,
                        data_={
                            "status": "success",
                            "chat": {
                                "id": chat.id,
                                "message": chat.message,
                                "timestamp": chat.timestamp,
                                "sender": {
                                    "id": chat.sender.id,
                                    "pseudonym": chat.sender.pseudonym,
                                    "username": chat.sender.username
                                }
                            }
                        }
                    )
            return json_response(
                status_=404,
                data_={
                    "status": "chat_sender_not_in_chatroom"
                }
            )
        return json_response(
            status_=404,
            data_={
                "status": "chat_sender_not_found"
            }
        )
    return json_response(
        status_=404,
        data_={
            "status": "chatroom_not_found"
        }
    )

@app.route('/chat/info', methods=['POST'])
@require_apikey
def chat_info():
    chatroom_id = int(request.json["chatroom_id"])
    chat_sender = int(request.json["chat_sender"])

    chatroom: Chatroom = db.get_chatroom(chatroom_id)
    chat_sender: User = db.get_user_id(chat_sender)
    if chatroom:
        if chat_sender:
            for i in chatroom.recipients:
                if i.id == chat_sender.id:
                    chats = []
                    for i in chatroom.chats:
                        if i.sender.id == chat_sender.id:
                            chats.append(
                                {
                                    "id": i.id,
                                    "timestamp": i.timestamp,
                                    "message": i.message
                                }
                            )
                    return json_response(
                        status_=200,
                        data_={
                            "status": "success",
                            "chats": chats
                        }
                    )
            return json_response(
                status_=404,
                data_={
                    "status": "chat_sender_not_in_chatroom"
                }
            )
        return json_response(
            status_=404,
            data_={
                "status": "chat_sender_not_found"
            }
        )
    return json_response(
        status_=404,
        data_={
            "status": "chatroom_not_found"
        }
    )
################ END CHAT BLUEPRINTS ################

################ SESSIONS BLUEPRINTS ################
@app.route('/session/invalidate', methods=['POST'])
@require_apikey
def session_invalidate():
    session_hash: str = str(request.json["session_hash"])

    session: Session = db.get_session(session_hash)
    if session:
        if db.del_session(session_hash):
            return json_response(
                status_=200,
                data_={
                    "status": "success",
                    "session": {
                            "id": session.id,
                            "valid_until": 0
                    }
                }
            )
        return json_response(
            status_=500,
            data_={
                "status": "failed_to_invalidate_session"
            }
        )
    return json_response(
        status_=404,
        data_={
            "status": "session_not_found"
        }
    )

@app.route('/sessions/data/add', methods=['POST'])
@require_apikey
def session_add_data():
    session_hash: str = str(request.json["session_hash"])
    data_key: str = str(request.json["data_key"])
    data_content: str = str(request.json["data_content"])

    session: Session = db.get_session(session_hash)
    session_data: SessionData = SessionData(key=data_key, data=data_content, valid_until=time.time() + 3600)
    
    if session:
        if session.add_data(session_data):
            return json_response(
                status_=200,
                data_={
                    "status": "success",
                    "session": {
                        "id": session.id,
                        "valid_until": session.valid_until
                    },
                    "data": session_data.__dict__
                }
            )
        return json_response(
            status_=500,
            data_={
                "status": "failed_to_add_data"
            }
        )
    return json_response(
        status_=404,
        data_={
            "status": "session_not_found"
        }
    )

@app.route('/session/data/all', methods=['POST'])
@require_apikey
def session_get_all_data():
    session_hash: str = str(request.json["session_hash"])

    session: Session = db.get_session(session_hash)
    if session:
        return json_response(
            status_=200,
            data_={
                "status": "success",
                "session": {
                    "id": session.id,
                    "valid_until": session.valid_until,
                    "session_data": [
                        {
                            "key": i.key,
                            "data" : i.data
                        } for i in session.session_data()
                    ]
                }
            }
        )
    return json_response(
        status_=404,
        data_={
            "status": "session_not_found"
        }
    )

@app.route('/session/data/info', methods=['POST'])
@require_apikey
def session_get_data():
    session_hash: str = str(request.json["session_hash"])
    data_key: str = str(request.json["data_key"])

    session: Session = db.get_session(session_hash)
    for i in session.session_data():
        if i.key == data_key:
            data: SessionData = i
    
    if session:
        if data:
            return json_response(
                status_=200,
                data_={
                    "status": "success",
                    "session": {
                        "id": session.id,
                        "valid_until": session.valid_until,
                    },
                    "data": data.__dict__
                }
            )
        return json_response(
            status_=404,
            data_={
                "status": "data_not_found"
            }
        )
    return json_response(
        status_=404,
        data_={
            "status": "session_not_found"
        }
    )

@app.route('/session/data/delete', methods=['POST'])
@require_apikey
def session_del_data():
    session_hash: str = str(request.json["session_hash"])
    data_key: str = str(request.json["data_key"])

    session: Session = db.get_session(session_hash)
    if session:
        if session.del_data(data_key):
            return json_response(
                status_=200,
                data_={
                    "status": "success"
                }
            )
        return json_response(
            status_=404,
            data_={
                "status": "key_not_found"
            }
        )
    return json_response(
        status_=404,
        data_={
            "status": "session_not_found"
        }
    )
############## END SESSIONS BLUEPRINTS ##############
