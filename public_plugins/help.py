import asyncio

print("[Public Plugin] <help.py>: This plugin helps you with commands.")


help_message = """

__**Basic Commands**__:

**!help** - prints this message.
"""


@asyncio.coroutine
def action(message, client, config):
    pass
