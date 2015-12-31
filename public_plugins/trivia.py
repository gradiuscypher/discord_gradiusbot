import asyncio

print("[Public Plugin] <trivia.py>: Trivia plugin.")


@asyncio.coroutine
def action(message, client):
    yield from client.send_message(message.channel, message.content)
