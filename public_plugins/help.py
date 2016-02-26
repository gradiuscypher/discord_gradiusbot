import asyncio

print("[Public Plugin] <help.py>: This plugin helps you with commands.")


help_message = """

__**Available Commands**__:

!help - prints this message.

!namecolor *[color]* - grants your user a different color name. Use it without a color to see a list of colors.
                    If your desired color does not exist, speak to a chat admin.

                    Can also use !namecolor random to pick a random color.
"""


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()
    bot_channel = config.get("BotSettings", "bot_channel")
    if len(split_content) > 0:
        if split_content[0] == "!help" and message.channel.name == bot_channel:
            yield from client.send_message(message.author, help_message)
