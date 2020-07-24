import time
import random
from hashlib import sha512

class User:
    def __init__(self, username: str, password: str, id: int = 0):
        self.id = id
        self.username = username
        self.password = password
        self.pseudonym = None

        self.update_pseudonym()
    
    def update_pseudonym(self):
        names = ["Alex", "Alessia", "Brad", "Belford", "Buds", "Conny", "Cris", "Chris", "Dennis", "Dolly", "Donnel", "Efra", "Essburn", "Emperor", "Fris", "Freskel", "Folly"]
        self.pseudonym = names[random.randint(0, len(names)-1)] + " " + names[random.randint(0, len(names)-1)]

class Chat:
    def __init__(self, id: int, sender: User, timestamp: float, message: str):
        self.id = id
        self.sender = sender
        self.timestamp = timestamp
        self.message = message

class Chatroom:
    def __init__(self, id: int):
        self.id = id
        self.recipients = set()
        self.chat = set()
    
    def add_recipients(self, user: User):
        self.recipients.add(user)
    
    def add_chat(self, chatMessage: Chat):
        self.chat.add(chatMessage)

class SessionData:
    def __init__(self, key: str, data, valid_until: float):
        self.key = key
        self.data = data
        self.valid_until = valid_until
    
    def get(self) -> set:
        return {
            "key": self.key,
            "data": self.data
        }

class Session:
    def __init__(self, id: int=0):
        self.id = id
        self.valid_until = str(time.time())

        random_code = "".join(["abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[random.randint(0, 51)] for _ in range(128)])
        random_person = ["erlangga", "aurelia", "michael", "ibrahim", "gabriele", "orlando", "wowotek", "benita", "mchlorlnd"][random.randint(0, 8)]

        self.session_hash = sha512((self.valid_until + random_code + random_person).encode("utf-8")).hexdigest()
        self.session_data = set()
    
    def add_data(self, data: SessionData) -> bool:
        try:
            self.session_data.add(data)
        except Exception as e:
            print(f"Error adding session data to session({self.id}): {e}", flush=True)
            return False
        return True
    
    def del_data(self, target_key: str) -> bool:
        try:
            for i in self.session_data:
                if i.key == target_key:
                    self.session_data.remove(i)
                    return True
            return False
        except Exception as e:
            print(f"Error deleteing session data at session({self.id}): {e}", flush=True)
            return False
    
    def get_data(self, target_key: str) -> SessionData:
        for i in self.session_data:
            if i.key == target_key:
                if time.time() >= i.valid_until:
                    return None 
                return i
        return None

