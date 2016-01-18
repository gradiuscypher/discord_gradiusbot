import asyncio

print("[Public Plugin] <amplitude_highscore.py>: This plugin helps track amplitude high scores via screenshot proof.")


@asyncio.coroutine
def action(message, client):
    # yield from client.send_message(message.channel, message.content)
