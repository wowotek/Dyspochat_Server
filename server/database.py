from .models import User, Chat, Chatroom
from typing import Set, List, Tuple, Union

class Database:
    def __init__(self):
        self.db_user: Set(User) = set()
        self.db_chat: Set(Chat) = set()
        self.db_chatroom: Set(Chatroom) = set()
    
    def get_user_last_id(self) -> int:
        last_id: int = 0
        for i in self.db_user:
            if i.id >= last_id:
                last_id = i.id
        
        return last_id + 1
    
    def get_user_id(self, id: int) -> Union(User, None):
        for i in self.db_user:
            if i.id == id:
                return i
    
    def get_user_username(self, username: str) -> Union(User, None):
        for i in self.db_user:
            if i.username == username:
                return i
    
    def get_user_all(self) -> List(User):
        return [i for i in self.db_user]

    def add_user(self, user: User) -> Tuple(bool, Union(User, None)):
        for i in self.db_user:
            if i.username == user.username:
                return (False, None)

        user.id = self.get_user_last_id()
        self.db_user.add(user)
        return (True, user)
    
    def del_user_id(self, id: int) -> Tuple(bool, Union(User, None)):
        user: User = None
        for i in self.db_user:
            if i.id == id:
                user = i
                self.db_user.remove(user)
                return (True, user)
        
        return (False, None)
    
    def del_user_username(self, username: str) -> Tuple(bool, Union(User, None)):
        user: User = None
        for i in self.db_user:
            if i.username == username:
                user = i
                self.db_user.remove(user)
                return (True, user)
        
        return (False, None)
        
    def edit_user(self, target_id: int, new_data: User) -> Tuple(bool, Union(User, None)):
        for i in self.db_user:
            if i.id == target_id:
                i.password = new_data.password
                return (True, i)
        
        return (False, None)