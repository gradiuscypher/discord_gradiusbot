import asyncio

print("[Public Plugin] <autodelete_botchannel.py>: This plugin autodeletes messages from a bot channel.")


@asyncio.coroutine
def action(message, client, config):
    config.get("BotSettings", "bot_channel")

    if message.channel.name == config.get('BotSettings', 'bot_channel'):
        yield from client.delete_message(message)
