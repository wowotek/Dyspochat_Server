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