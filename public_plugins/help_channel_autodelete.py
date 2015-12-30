import configparser
import asyncio

print("[Public Plugin] <help_channel_autodelete.py>: This plugin deletes messages from a bot help channel.")

config = configparser.RawConfigParser()
config.read('config.conf')


@asyncio.coroutine
def action(message, client):
    if message.channel.name == config.get('BotSettings', 'bot_channel'):
        yield from client.delete_message(message)
