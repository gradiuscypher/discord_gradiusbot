import asyncio
import discord
from discord import Embed, Color

print("[Private Plugin] <pm_to_channel.py>: This plugin forwards PMs to a Discord channel.")

"""
config options:
[Pokemon]
forward_chan = (channel to forward to)
forward_server = (server ID to forward to)
account_forward_from = (account ID to forward from)
"""


@asyncio.coroutine
def action(message, client, config):
    forward_chan = config.get('Pokemon', 'forward_chan')
    account_forward_from = config.get('Pokemon', 'account_forward_from')

    if message.author.id == account_forward_from and len(message.embeds) > 0:
        message_embed = message.embeds[0]
        pokemon_name = message_embed['title'].split()[0]
        split_description = message_embed['description'].split("\n")
        pokemon_location = split_description[0].replace('alert-', '')
        pokemon_time = split_description[3].split("remaining.")[0] + " left."
        map_icon = message_embed['image']['url']
        map_url = message_embed['url']

        # Build the new Embed
        description = pokemon_location + "\n" + pokemon_time
        send_embed = Embed(title=pokemon_name, color=Color.green())
        send_embed.url = map_url
        send_embed.set_image(url=map_icon)
        send_embed.description = description

        target_channel = discord.utils.get(client.get_all_channels(), name=forward_chan)
        yield from client.send_message(target_channel, embed=send_embed)
