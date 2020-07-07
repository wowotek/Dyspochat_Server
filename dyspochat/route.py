from flask_json import json_response, request

from . import app
from .controller import *
from .model import *


@app.route("/user/registration", methods=["POST"])
def user_registration():
    username = request.form["reg_username"]
    password = request.form["reg_password"]

    status = add_user(username, password)
    if status[0]:
        return json_response(
            act_status=True,
            user={
                "id": status[1].id,
                "username": status[1].username
            },
            cause=""
        )
    else:
        return json_response(act_status=False, user={}, cause=status[1])

@app.route("/user/login", methods=["POST"])
def user_login():
    username = request.form["log_username"]
    password = request.form["log_password"]

    user = get_user_username(username)
    if user == None:
        return json_response(
            act_status=False,
            user={},
            cause="user_invalid"
        )
    else:
        if user.password == password:
            return json_response(
                act_status=True,
                user={
                    "id": user.id,
                    "username": user.username
                },
                cause=""
            )
        return json_response(
            act_status=False,
            user={},
            cause="pass_invalid"
        )

@app.route("/chat/create", methods=["POST"])
def chat_create():
    user_id = request.form["user_id"]

    user = get_user_id(int(user_id))
    if(user == None):
        return json_response(act_status=False, chat={}, cause="user_invalid")
    else:
        chat = create_chat(user)

        if chat[0]:
            chatroom = chat[1][0]
            recipient = chat[1][1]

            return json_response(
                act_status=True,
                data={
                    "chatroom": {
                        "id": chatroom.id,
                        "room_id": chatroom.room_id
                    },
                    "recipient": {
                        "id": recipient.id,
                        "user_id": recipient.user.id
                    }
                },
                cause=""
            )
        else:
            return json_response(
                act_status=False,
                data={},
                cause=""
            )

@app.route("/chat/join", methods=["POST"])
def chat_join():
    room_id = request.form["room_id"]
    user_id = int(request.form["user_id"])
    
    # check if user already exist
    for i in ChatRecipient.query.all():
        if i.chatroom.room_id == str(room_id):
            if i.user_id == int(user_id):
                return json_response(
                    act_status=False,
                    chatroom={},
                    cause="user_in_chatroom"
                )

    chatroom = get_chatroom_room_id(room_id)
    user=get_user_id(int(user_id))
    if chatroom != None:
        join_status = add_recipient(chatroom=chatroom, user=user)
        if join_status[0]:
            return json_response(
                act_status=True,
                chatroom={
                    "id": chatroom.id,
                    "room_id": chatroom.room_id
                },
                cause=""
            )
        return json_response(
            act_status=False,
            chatroom={},
            cause="server_error"
        )
    return json_response(
        act_status=False,
        chatroom={},
        cause="chatroom_invalid"
    )

@app.route("/chat/leave", methods=["POST"])
def chat_leave():
    room_id = request.form["room_id"]
    user_id = int(request.form["user_id"])

    chatroom = get_chatroom_room_id(room_id)
    user=get_user_id(int(user_id))
    if chatroom != None:
        join_status = remove_recipient(chatroom=chatroom, user=user)
        if join_status[0]:
            return json_response(
                act_status=True,
                cause=""
            )
        return json_response(
            act_status=False,
            cause="server_error"
        )
    return json_response(
        act_status=False,
        cause="chatroom_invalid"
    )

@app.route("/chat/get_room_recipient", methods=["POST"])
def get_room_recipient():
    room_id = request.form["room_id"]

    return json_response(
        act_status=True,
        recipients=[
            {
                "id": i.id,
                "username": i.username
            } for i in get_recipient_in_room(str(room_id))
        ]
    )

@app.route("/chat/create_session", methods=["POST"])
def start_session():
    room_id = request.form["room_id"]
    user_id = int(request.form["user_id"])

    allowed_port = [5250 + i for i in range(4000)]