import asyncio

note = """
NOTE: This plugin is written to be used on a bot that is only in a single server.
This plugin will not function properly on a bot that's a member of more than one server.
"""

print("[Private Plugin] <ticket.py>: This plugin tracks tickets created by users for things like reports.")
print("[Private Plugin] {}".format(note))


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()

    if len(split_content) > 0:
        if split_content[0] == "!ticket":
            yield from client.send_message(message.author, "")
