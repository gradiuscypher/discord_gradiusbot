import configparser


config = configparser.RawConfigParser()
config.read('config.conf')

help_message = """
Commands must be sent to the bot channel where they will be removed afterwards.

__**Available Commands**__:

**namecolor** *[color]* - grants your user a different color name. Use it without a color to see a list of colors.
                    If your desired color does not exist, speak to a chat admin.
"""


def action(message, client):
    split_content = message.content.split()

    if split_content[0] == "help" and message.channel.name == config.get('Settings', 'bot_channel'):
        client.send_message(message.author, help_message)
