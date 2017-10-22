import asyncio
import discord
import json
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

    if message.author.id == account_forward_from:
        # Parse the information
        json_blob = json.loads(message.content)
        map_url = json_blob['url']
        map_image_url = json_blob['image']['url']

        # Pull out Pokemon Information
        split_title = json_blob['title'].split()
        pokemon_name = split_title[0]
        pokemon_iv_percent = split_title[1]
        pokemon_cp = split_title[2]
        pokemon_stats = split_title[3]

        # Pull out Description information
        split_description = json_blob['description'].split('\n')
        location = split_description[0]
        alert_name = split_description[1].split('alert-')[1].replace('-', ' ')
        moves = split_description[2]
        spawn_time = split_description[4]

        # Get the Thumbnail URL
        pokemon_thumbnail_url = json_blob['thumbnail']['proxy_url']

        # Build the new Embed
        embed_title = pokemon_name + " - " + pokemon_iv_percent + " - " + pokemon_cp
        pokemon_embed = Embed(title=embed_title, color=Color.green())
        pokemon_embed.add_field(name="Alert", value=alert_name, inline=True)
        pokemon_embed.add_field(name="Location", value=location, inline=True)
        pokemon_embed.add_field(name="Moves", value=moves, inline=True)
        pokemon_embed.add_field(name="Stats", value=pokemon_stats, inline=True)
        pokemon_embed.add_field(name="Spawn Timer", value=spawn_time, inline=True)
        pokemon_embed.set_thumbnail(url=pokemon_thumbnail_url)
        pokemon_embed.set_image(url=map_image_url)
        pokemon_embed.url = map_url

        target_channel = discord.utils.get(client.get_all_channels(), name=forward_chan)
        target_role = discord.utils.get(target_channel.server.roles, name="rares")

        # Notification For 100% IV
        if pokemon_iv_percent == '100%':
            message_content = '<@&' + target_role.id + '>'
            yield from client.send_message(target_channel, message_content)

        yield from client.send_message(target_channel, embed=pokemon_embed)
        # yield from client.send_message(message.author, embed=pokemon_embed)
