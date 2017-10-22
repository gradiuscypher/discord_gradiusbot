import asyncio
import discord
import json

print("[Private Plugin] <forward_pm.py>: This plugin forwards PMs to another Discord account.")

"""
config options:
[Pokemon]
forward_target = (account to forward to)
forward_from = (account string match to forward from)
forward_discrim = (account discrim)
"""


@asyncio.coroutine
def action(message, client, config):
    forward_target = config.get('Pokemon', 'forward_target')
    forward_from = config.get('Pokemon', 'forward_from')
    forward_discrim = config.get('Pokemon', 'forward_discrim')

    if forward_from.lower() in str(message.author).lower():
        members = client.get_all_members()
        forward_target_obj = discord.utils.get(members, name=forward_target, discriminator=forward_discrim)

        if len(message.embeds) > 0:
            message_embed = message.embeds[0]
            message_json = json.dumps(message_embed)
            print(repr(message_json))

            yield from client.send_message(forward_target_obj, message_json)
