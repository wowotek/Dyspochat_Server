import time
from typing import Set, List, Tuple, Union

from .models import User, Chat, Chatroom, Session, SessionData

class Database:
    def __init__(self):
        self.db_user: Set[User] = set()
        self.db_chatroom: Set[Chatroom] = set()
        self.db_chat: Set[Chat] = set()
        self.db_session: Set[Session] = set()
        self.db_apikey: Set[str] = set()

    def add_sanity_check_data(self):
        #### Add Testing Data for Sanity Check ####
        test_user_1 = User("test_user_1", "test_password")
        test_user_2 = User("test_user_2", "test_password")
        self.add_user(test_user_1)
        self.add_user(test_user_2)

        test_chatroom = self.add_chatroom()
        test_chatroom = self.get_chatroom(test_chatroom.id)
        test_chatroom.add_recipients(self.get_user_id(test_user_1.id))
        test_chatroom.add_recipients(self.get_user_id(test_user_2.id))

        test_chat_1 = Chat(0, test_user_1, time.time(), "test chat from test_user_1 to test_user_2")
        test_chat_2 = Chat(1, test_user_2, time.time(), "test chat from test_user_2 to test_user_1")
        test_chatroom = self.get_chatroom(test_chatroom.id)
        test_chatroom.add_chat(test_chat_1)
        test_chatroom.add_chat(test_chat_2)

        test_sess = Session(id=0)
        test_sess.session_hash = "test_session_hash"
        test_sess.valid_until = -1
        test_sess.add_data(SessionData("test_key_1", "test_value_string", -1))
        test_sess.add_data(SessionData("test_key_2", 12345672945702348, -1))
        test_sess.add_data(SessionData("test_key_3", 69.420, -1))
        test_sess.add_data(SessionData("test_key_4", True, -1))
        test_sess.add_data(SessionData("test_key_5", {"data_1": "data1", "data_2": 2}, -1))
        
        self.db_session.add(test_sess)
        self.db_apikey.add("test_api_key")

        return {
            "users": {
                "test_user_1": test_user_1.__dict__,
                "test_user_2": test_user_2.__dict__
            },
            "chatroom": {
                "id": test_chatroom.id,
                "chats": len(test_chatroom.chats),
                "recipients": len(test_chatroom.recipients)
            },
            "chats": {
                "test_chat_1": {
                    "id": test_chat_1.id,
                    "username": test_chat_1.sender.username,
                    "message": test_chat_1.message
                },
                "test_chat_2": {
                    "id": test_chat_2.id,
                    "username": test_chat_2.sender.username,
                    "message": test_chat_2.message
                }
            },
            "session": {
                "id": test_sess.id,
                "valid_until": test_sess.valid_until,
                "hash": test_sess.session_hash,
                "data": [
                    {
                        "key": i.key,
                        "data": i.data,
                        "valid_until": i.valid_until
                    } for i in test_sess.session_data
                ]
            },
            "apikey": "test_api_key"
        }
        ###########################################
    
    def remove_sanity_check_data(self, sanity_data: dict) -> bool:
        try:
            print("Deleting User 1")
            self.del_user_id(sanity_data["users"]["test_user_1"]["id"])
            print("Deleting User 2")
            self.del_user_id(sanity_data["users"]["test_user_2"]["id"])
            print("Deleting Chatroom")
            self.delete_chatroom(sanity_data["chatroom"]["id"])
            print("Deleting Session")
            self.del_session(sanity_data["session"]["hash"])
            return True
        except Exception as e:
            print(f"failed to remove sanity data {e}")
        return False
        
    ### USER API ###
    def get_user_last_id(self) -> int:
        last_id: int = 0
        for i in self.db_user:
            if i.id >= last_id:
                last_id = i.id
        
        return last_id + 1
    
    def get_user_id(self, id: int) -> Union[User, None]:
        for i in self.db_user:
            if i.id == id:
                return i
    
    def get_user_username(self, username: str) -> Union[User, None]:
        for i in self.db_user:
            if i.username == username:
                return i
    
    def get_user_all(self) -> List[User]:
        return [i for i in self.db_user]

    def add_user(self, user: User) -> Tuple[bool, Union[User, None]]:
        try:
            for i in self.db_user:
                if i.username == user.username:
                    return (False, None)

            user.id = self.get_user_last_id()
            self.db_user.add(user)
            return (True, user)
        except Exception as e:
            print(f"Failed to add user : {e}")
        return (False, None)
    
    def del_user_id(self, id: int) -> Tuple[bool, Union[User, None]]:
        try:
            user: User = None
            for i in self.db_user:
                if i.id == id:
                    user = User(username=i.username, password=i.password, id=i.id)
                    self.db_user.remove(i)
                    return (True, user)
            
            return (False, None)
        except Exception as e:
            print(f"Failed to delete user_id: {e}")
        return (False, None)
    
    def del_user_username(self, username: str) -> Tuple[bool, Union[User, None]]:
        try:
            user: User = None
            for i in self.db_user:
                if i.username == username:
                    user = i
                    self.db_user.remove(user)
                    return (True, user)
            
            return (False, None)
        except Exception as e:
            print(f"Failed to delete user_username: {e}")
        return (False, None)
        
    def edit_user(self, target_id: int, new_data: User) -> Tuple[bool, Union[User, None]]:
        for i in self.db_user:
            if i.id == target_id:
                i.password = new_data.password
                return (True, i)
        
        return (False, None)
    ### END USER API ###
    
    ### CHATROOM API ###
    def get_chatroom_last_id(self) -> int:
        last_id: int = 0
        for i in self.db_chatroom:
            if i.id >= last_id:
                last_id = i.id
        
        return last_id
    
    def get_chatroom(self, target_id: int) -> Union[Chatroom, None]:
        for i in self.db_chatroom:
            if i.id == target_id:
                return i
        return None
    
    def add_chatroom(self) -> Union[Chatroom, None]:
        try:
            chatroom: Chatroom = Chatroom(self.get_chatroom_last_id() + 1)
            self.db_chatroom.add(chatroom)
            return chatroom
        except Exception as e:
            print(f"Error adding chatroom: {e}")
        return None

    def delete_chatroom(self, target_id: int) -> Union[Chatroom, None]:
        for i in self.db_chatroom:
            if i.id == target_id:
                chatroom = Chatroom(id=i.id)
                chatroom.chat = i.chats
                chatroom.recipients = i.recipients
                self.db_chatroom.remove(i)
                return chatroom
        return None
    ### END CHATROOM API ###

    ### CHAT API ###
    def get_chat_last_id(self, chatroom_id: int) -> int:
        last_id: int = 0
        for i in self.db_chatroom:
            if i.id == chatroom_id:
                for j in i.chats:
                    if j.id >= last_id:
                        last_id = j.id
                return last_id
    ### END CHAT API ###

    ### SESSION API ###
    def add_session(self) -> Session:
        last_id: int = 0
        for i in self.db_session:
            if i.id >= last_id:
                last_id = i.id
        
        session = Session(last_id+1)
        self.db_session.add(session)
        return session
    
    def get_session(self, session_hash: str) -> Union[Session, None]:
        for i in self.db_session:
            if i.session_hash == session_hash:
                return i

    def get_session_all(self) -> List[Session]:
        return [i for i in self.db_session]
    
    def del_session(self, session_hash: str) -> bool:
        try:
            for i in self.db_session:
                if i.session_hash == session_hash:
                    self.db_session.remove(i)
                    return True
            return False
        except Exception as e:
            print(f"Failed to delete Session : {e}")
        return False
    ### END SESSION API ###
