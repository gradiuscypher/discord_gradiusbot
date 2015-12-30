import time
import asyncio
from threading import Thread

print("[Public Plugin] <sleep.py>: This plugin makes your bot sleep for a period of time.")

@asyncio.coroutine
def action(message, client):
    split_content = message.content.split()

    if split_content[0] == "!sleep":
        print("Yielding")
        yield from client.send_message(message.channel, "Sleeping.")
        print("Sleeping")
        t = Thread(target=long_sleep, args=(int(split_content[1]),))
        t.start()
        while t.is_alive():
            yield from asyncio.sleep(1)
            print("Still sleeping.")
        print("Yielding")
        yield from client.send_message(message.channel, "Awake.")
        print("Awake")

    else:
        yield from client.send_message(message.channel, message.content)


def long_sleep(n):
    time.sleep(n)
