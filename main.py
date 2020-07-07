import asyncio

from dyspochat import app
from dyspochat.chat_handler import listener, updater, registrar


async def run_server(future):
    try:
        app.run(host="0.0.0.0", port=2345, debug=True)
    except Exception as e:
        future.set_result(e)
    finally:
        future.set_result("Done")

loop = asyncio.get_event_loop()
loop.run_until_complete(updater)
loop.run_until_complete(listener)
loop.run_until_complete(registrar)
loop.run_forever()