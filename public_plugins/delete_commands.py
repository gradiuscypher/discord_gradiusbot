import asyncio

print("[Public Plugin] <delete_commands.py>: This plugin deletes messages from a channel if it starts with !.")


@asyncio.coroutine
def action(message, client, config):
    if message.content.startswith("!"):
        yield from client.delete_message(message)
