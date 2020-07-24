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

        self._add_sanity_check_data()

    def _add_sanity_check_data(self):
        #### Add Testing Data for Sanity Check ####
        test_user_1 = User("test_user_1", "test_password", id=0)
        test_user_2 = User("test_user_2", "test_password", id=1)
        self.add_user(test_user_1)
        self.add_user(test_user_2)

        test_chatroom = Chatroom(0)
        test_chatroom.add_recipients(test_user_1)
        test_chatroom.add_recipients(test_user_2)
        # TODO: SANITY_CHECK/CHATROOM: first, add chatroom to database using database api
        # TODO: SANITY_CHECK/CHATROOM: second, get chatroom using database api
        # TODO: SANITY_CHECK/CHATROOM: third, use get user from database api for adding recipients to test room

        test_chat_1 = Chat(0, test_user_1, time.time(), "test chat from test_user_1 to test_user_2")
        test_chat_2 = Chat(1, test_user_2, time.time(), "test chat from test_user_2 to test_user_2")
        test_chatroom.add_chat(test_chat_1)
        test_chatroom.add_chat(test_chat_2)
        # TODO: SANITY_CHECK/CHAT: first get chatroom using database api
        # TODO: SANITY_CHECK/CHAT: add test chat to chatroom which just got

        test_sess = Session(id=0)
        test_sess.session_hash = "test_session_hash"
        test_sess.valid_until = -1
        test_sess.add_data(SessionData("test_key_1", "test_value_string", -1))
        test_sess.add_data(SessionData("test_key_2", 12345672945702348, -1))
        test_sess.add_data(SessionData("test_key_3", 69.420, -1))
        test_sess.add_data(SessionData("test_key_4", True, -1))
        test_sess.add_data(SessionData("test_key_4", {"data_1": "data1", "data_2": 2}, -1))
        
        self.db_session.add(test_sess)
        self.db_apikey.add("test_api_key")
        ###########################################
    
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

    def get_session_all(self, session_hash: str) -> List[Session]:
        return [i for i in self.db_session]
    ### END SESSION API ###

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
        for i in self.db_user:
            if i.username == user.username:
                return (False, None)

        user.id = self.get_user_last_id()
        self.db_user.add(user)
        return (True, user)
    
    def del_user_id(self, id: int) -> Tuple[bool, Union[User, None]]:
        user: User = None
        for i in self.db_user:
            if i.id == id:
                user = User(username=i.username, password=i.password, id=i.id)
                self.db_user.remove(i)
                return (True, user)
        
        return (False, None)
    
    def del_user_username(self, username: str) -> Tuple[bool, Union[User, None]]:
        user: User = None
        for i in self.db_user:
            if i.username == username:
                user = i
                self.db_user.remove(user)
                return (True, user)
        
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
        except Exception as e:
            print(f"Error adding chatroom: {e}")
            return None
        return chatroom

    def delete_chatroom(self, target_id: int) -> Union[Chatroom, None]:
        for i in self.db_chatroom:
            if i.id == target_id:
                chatroom = Chatroom(id=i.id)
                chatroom.chat = i.chat
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
                for j in i.chat:
                    if j.id >= last_id:
                        last_id = j.id
                return last_id
    ### END CHAT API ###

    ### SESSION API ###
    # TODO: DATABASE_API/SESSION: implement all session required API
    ### END SESSION API ###