import asyncio

note = """
NOTE: This plugin is written to be used on a bot that is only in a single server.
This plugin will not function properly on a bot that's a member of more than one server.
"""

print("[Private Plugin] <help.py>: This plugin helps you with commands.")
print("[Private Plugin] {}".format(note))


help_message = """

__**Basic Commands**__:

**!help** - prints this message.
"""


@asyncio.coroutine
def action(message, client, config):
    pass
