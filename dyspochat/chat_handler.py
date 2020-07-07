import asyncio
import datetime
import random
import websockets
import json

from .controller import *

CLIENT = set()

# On Message Update ----
async def message_updater(websocket, path):
    while True:
        await websocket.send(" ".join([i.username for i in get_user_all()]))
        await asyncio.sleep(0.25)

# On Message Received
async def message_listener(websocket, path):
    while True:
        
        await asyncio.sleep(0.25)


updater = websockets.serve(message_updater, "127.0.0.1", 5678)
listener = websockets.serve(message_listener, "127.0.0.1", 5679)