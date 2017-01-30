import asyncio

print("[Private Plugin] <example.py>: This plugin echoes details back to the sender.")


@asyncio.coroutine
def action(message, client, config):
    print("This is a private message")
    print("This is the sender:", message.author)
    print("This is the message:", message.content)
    yield from client.send_message(message.channel, "Your message: " + message.content)
