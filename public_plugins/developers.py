import asyncio
import json
import random

print("[Public Plugin] <developers.py>: This plugin DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS.")


@asyncio.coroutine
def action(message, client, config):
    developers_string = "DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS DEVELOPERS!"

    if config.has_option("developers", "chance"):
        chance = config.getint("developers", "chance")
    else:
        chance = 1

    if config.has_option("developers", "permitted_channels"):
        permitted_channels = json.loads(config.get('developers', 'permitted_channels'))
    else:
        permitted_channels = []

    dice = random.randint(1, 100)

    if "developer" in message.content.lower() and message.channel.name in permitted_channels and dice <= chance:
        yield from client.send_message(message.channel, developers_string)
