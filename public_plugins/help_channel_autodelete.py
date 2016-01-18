import configparser
import asyncio

print("[Public Plugin] <help_channel_autodelete.py>: This plugin deletes messages from a bot help channel.")


@asyncio.coroutine
def action(message, client, config):
    if message.channel.name == config.get('BotSettings', 'bot_channel'):
        yield from client.delete_message(message)
