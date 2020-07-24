from functools import wraps

from flask import jsonify, request, abort
from flask_json import json_response

from . import app, db
from .models import User, Chat, Chatroom, Session, SessionData


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
    return json_response(data_='pong!')

@app.route('/misc/hello', methods=['GET'])
@require_apikey
def apikey_check():
    # TODO: ENDPOINTS/MISC: make sure @require_apikey is sane -> properly checking database for valid apikey
    return json_response(data_="world")

@app.route('/misc/sane', methods=['GET'])
@require_apikey
def sanity_check():
    # TODO: ENDPOINTS/MISC: implement sanity check, check wheter all the database api is correct using mockup data provided by database
    return json_response(data_="i am sane")
################ END MISC BLUEPRINTS ################

################## USER BLUEPRINTS ##################
@app.route('/user', methods=['PUT'])
@require_apikey
def user_register():
    username: str = str(request.form.get("username", type=str))
    password: str = str(request.form.get("password", type=str))

    add_status = db.add_user(User(username, password))
    if add_status[0]:
        return json_response(
            data_={
                "status": "register_success",
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
    username: str = str(request.form.get("username", type=str))
    password: str = str(request.form.get("password", type=str))

    user: User = db.get_user_username(username)
    if user != None:
        if user.password == password:
            session: Session = db.add_session()
            return json_response(
                data_={
                    "status": "login_success",
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
    user_id: int = int(request.form.get("user_id", type=int, default=-1))
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
    user_id: int = int(request.form.get("user_id", type=int, default=-1))
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
    # TODO: ENDPOINTS/CHATROOM: Implement add chatroom
    ...

@app.route('/chatroom', methods=['GET'])
@require_apikey
def chatroom_get():
    # TODO: ENDPOINTS/CHATROOM: Implement get chatroom info
    ...

@app.route('/chatroom', methods=['DELETE'])
@require_apikey
def chatroom_delete():
    # TODO: ENDPOINTS/CHATROOM: Implement deleting chatroom
    ...

@app.route('/chatroom', methods=['POST'])
@require_apikey
def chatroom_add_recipients():
    # TODO: ENDPOINTS/CHATROOM: Implement add recipients to chatroom
    ...

@app.route('/chatroom', methods=['PATCH'])
@require_apikey
def chatroom_del_recipients():
    # TODO: ENDPOINTS/CHATROOM: Implement deleting recipient from chatroom, reconsider: is this required ?
    ...
############## END CHATROOM BLUEPRINTS ##############

################## CHAT BLUEPRINTS ##################
@app.route('/chat', methods=['PUT'])
@require_apikey
def chat_add():
    # TODO: ENDPOINTS/CHAT: Implement add chat to the chatroom
    ...

@app.route('/chat', methods=['GET'])
@require_apikey
def chat_get():
    # TODO: ENDPOINTS/CHAT: Implement get chat information
    ...
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