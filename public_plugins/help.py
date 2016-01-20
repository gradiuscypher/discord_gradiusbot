import asyncio

print("[Public Plugin] <help.py>: This plugin helps you with commands.")


help_message = """

__**Available Commands**__:

!help - prints this message.

!namecolor *[color]* - grants your user a different color name. Use it without a color to see a list of colors.
                    If your desired color does not exist, speak to a chat admin.
"""


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()

    if split_content[0] == "!help":
        yield from client.delete_message(message)
        yield from client.send_message(message.author, help_message)
