import asyncio
import datetime

print("[Public Plugin] <print_message.py>: This plugin prints messages to the command line.")


@asyncio.coroutine
def action(message, client):
    time = datetime.datetime.now()
    print("[" + str(time) + "] <", message.author, "> :", message.content)
