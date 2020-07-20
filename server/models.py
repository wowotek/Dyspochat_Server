from hashlib import sha512

class User:
    def __init__(self, id: int, username: str, password: str = None):
        self.id = id
        self.username = username

        if password != None:
            self.password = sha512(password.encode("utf-8")).hexdigest()

class Chatroom:
    def __init__(self, id: int):
        self.id = id
        self.users = set()
        self.chat = set()

class Chat:
    def __init__(self, id: int, sender: User, timestamp: float, message: str):
        self.id = id
        self.sender = sender
        self.timestamp = timestamp
        self.message = message