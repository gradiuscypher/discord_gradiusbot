import asyncio

print("[Public Plugin] <echo.py>: This plugin echoes stuff to a public channel.")


@asyncio.coroutine
def action(message, client):
    yield from client.send_message(message.channel, message.content)
