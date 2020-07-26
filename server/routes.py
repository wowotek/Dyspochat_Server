import time
from functools import wraps

from flask import jsonify, request, abort
from flask_json import json_response

from . import app, db
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
        if request.headers.get('x-session-key') and request.headers.get('x-session-key') == "wowotek-key":
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function
############### END SESSION DECORATOR ###############

################## MISC BLUEPRINTS ##################
@app.route('/misc/ping', methods=['GET'])
def ping():
    return json_response(
        data_={
            "status": "success",
            "message": "pong!"
        }
    )

@app.route('/misc/hello', methods=['GET'])
@require_apikey
def apikey_check():
    return json_response(
        data_={
            "status": "success",
            "message": "world"
        }
    )

@app.route('/misc/sane', methods=['GET'])
@require_apikey
def sanity_check():
    sanity_data = db.add_sanity_check_data()
    print(sanity_data)
    if db.remove_sanity_check_data(sanity_data):
        return json_response(
            data_={
                "status": "success",
                "message": "i_am_sane",
                "sanity_data": sanity_data
            }
        )
    return json_response(
        data_={
            "status": "failed",
            "message": "i am insane"
        }
    )

@app.route('/misc/pseudonym', methods=['GET'])
def get_pseudonym():
    return json_response(
        data_={
            "status": "success",
            "pseudonym": generate_pseudonym()
        }
    )

################ END MISC BLUEPRINTS ################

################## USER BLUEPRINTS ##################
@app.route('/user', methods=['PUT'])
@require_apikey
def user_register():
    username: str = str(request.json["username"])
    password: str = str(request.json["password"])

    add_status = db.add_user(User(username, password))
    if add_status[0]:
        return json_response(
            data_={
                "status": "success",
                "user": {
                    "id": add_status[1].id,
                    "username": add_status[1].username
                }
            }
        )

    return json_response(
            data_={
                "status": "username_already_exist"
            }
        )


@app.route('/user', methods=['POST'])
@require_apikey
def user_login():
    username: str = str(request.json["username"])
    password: str = str(request.json["password"])

    user: User = db.get_user_username(username)
    if user != None:
        if user.password == password:
            session: Session = db.add_session()
            return json_response(
                data_={
                    "status": "success",
                    "session": {
                        "id": session.id,
                        "key": session.session_hash
                    }
                }
            )
        return json_response(
            data_={
                "status": "auth_failed"
            }
        )
    return json_response(
        data_={
            "status": "user_not_found"
        }
    )

@app.route('/user', methods=['DELETE'])
@require_apikey
def user_unregister():
    user_id: int = int(request.json["user_id"])
    status = db.del_user_id(user_id)

    if status[0]:
        return json_response(
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
        data_={
            "status": "user_not_found"
        }
    )

@app.route('/user', methods=['GET'])
@require_apikey
def user_get():
    user_id: int = int(request.json["user_id"])
    user: User = db.get_user_id(user_id)

    if user == None:
        return json_response(
            data_={
                "status": "user_not_found"
            }
        )

    return json_response(
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
@app.route('/chatroom', methods=['PUT'])
@require_apikey
def chatroom_add():
    chatroom: Chatroom = db.add_chatroom()
    if chatroom:
        return json_response(
            data_={
                "status": "success",
                "chatroom": {
                    "id": chatroom.id
                }
            }
        )
    return json_response(
        data_={
            "status": "chatroom_internal_server_error"
        }
    )

@app.route('/chatroom', methods=['GET'])
@require_apikey
def chatroom_info():
    print("chatroom_info", request.json)
    chatroom_id = int(request.json["chatroom_id"])

    chatroom: Chatroom = db.get_chatroom(chatroom_id)
    if chatroom:
        return json_response(
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
        data_={
            "status": "chatroom_not_found"
        }
    )

@app.route('/chatroom', methods=['DELETE'])
@require_apikey
def chatroom_delete():
    chatroom_id = int(request.json["chatroom_id"])

    chatroom = db.delete_chatroom(chatroom_id)
    if chatroom:
        return json_response(
            data_={
                "status": "success",
                "chatroom": {
                    "id": chatroom.id,
                    "chats": chatroom.chats,
                    "recipients": chatroom.recipients
                }
            }
        )
    return json_response(
        data_={
            "status": "chatroom_not_found"
        }
    )

@app.route('/chatroom', methods=['POST'])
@require_apikey
def chatroom_add_recipients():
    print("chatroom_add_recipients", request.json)
    chatroom_id = int(request.json["chatroom_id"])
    recipient_id = int(request.json["recipient_id"])

    chatroom: Chatroom = db.get_chatroom(chatroom_id)
    recipient: User = db.get_user_id(recipient_id)

    if chatroom:
        if recipient:
            # check if recipient already exist
            for i in chatroom.recipients:
                if i.id == recipient.id:
                    return json_response(
                        data_={
                            "status": "recipient_already_exist"
                        }
                    )
            chatroom.add_recipients(recipient)
            return json_response(
                data_={
                    "status": "success"
                }
            )
        return json_response(
            data_={
                "status": "recipient_not_found"
            }
        )
    return json_response(
        data_={
            "status": "chatroom_not_found"
        }
    )


@app.route('/chatroom', methods=['PATCH'])
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
                    chatroom.recipients.remove(i)
                    return json_response(
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
                data_={
                    "status": "recipient_not_in_chatroom"
                }
            )
        return json_response(
            data_={
                "status": "recipient_not_found"
            }
        )
    return json_response(
        data_={
            "status": "chatroom_not_found"
        }
    )
############## END CHATROOM BLUEPRINTS ##############

################## CHAT BLUEPRINTS ##################
@app.route('/chat', methods=['PUT'])
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
                    chat: Chat = Chat(db.get_chat_last_id(chatroom.id) + 1, chat_sender, time.time(), chat_message)
                    chatroom.add_chat(chat)
                    return json_response(
                        data_={
                            "status": "success"
                        }
                    )
            return json_response(
                data_={
                    "status": "chat_sender_not_in_chatroom"
                }
            )
        return json_response(
            data_={
                "status": "chat_sender_not_found"
            }
        )
    return json_response(
        data_={
            "status": "chatroom_not_found"
        }
    )

@app.route('/chat', methods=['GET'])
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
                        data_={
                            "status": "success",
                            "chats": chats
                        }
                    )
            return json_response(
                data_={
                    "status": "chat_sender_not_in_chatroom"
                }
            )
        return json_response(
            data_={
                "status": "chat_sender_not_found"
            }
        )
    return json_response(
        data_={
            "status": "chatroom_not_found"
        }
    )
################ END CHAT BLUEPRINTS ################

################ SESSIONS BLUEPRINTS ################
@app.route('/sessions', methods=['PUT'])
@require_apikey
def session_add_data():
    # TODO: ENDPOINTS/SESSIONS: Implement add data to specific session
    ...

@app.route('/session', methods=['GET'])
@require_apikey
def session_get_data():
    # TODO: ENDPOINTS/SESSIONS: Implement get data from specific session
    ...

@app.route('/session', methods=['DELETE'])
@require_apikey
def session_del_data():
    # TODO: ENDPOINTS/SESSIONS: Implement delete data from session
    ...

@app.route('/session', methods=['PURGE'])
@require_apikey
def session_invalidate():
    # TODO: ENDPOINTS/SESSIONS: Implement session invalidation (logout)
    ...
############## END SESSIONS BLUEPRINTS ##############
