import asyncio

note = """
NOTE: This plugin is written to be used on a bot that is only in a single server.
This plugin will not function properly on a bot that's a member of more than one server.
"""

print("[Private Plugin] <help.py>: This plugin helps you with commands.")
print("[Private Plugin] {}".format(note))


help_message = """

__**Available Commands**__:

**!help** - prints this message.

**!namecolor** *color* - grants your user a different color name. Use it without a color to see a list of colors.
                    If your desired color does not exist, speak to a chat admin.

                    Can also use **!namecolor** *random* to pick a random color.

**!join** *group* - allows you to join optional groups.
                You can use !join without a group to see a list of joinable groups.

**!leave** *group* - allows you to leave optional groups.
                You can use !leave without a group to see a list of leavable groups.
"""


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()
    if len(split_content) > 0:
        if split_content[0] == "!help":
            yield from client.send_message(message.author, help_message)
