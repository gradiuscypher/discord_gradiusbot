import asyncio
import re
import discord
import datetime
import traceback
import json
from discord import Embed, Color


print("[Private Plugin] <pokelerts.py>: This plugin forwards PokemonGo Alerts.")

"""
config options:
[Pokemon]
forward_chan = (channel to forward to)
forward_names = (account strings match to forward from)
production = False (whether the message should be sent to a channel or as a test PM)
"""


@asyncio.coroutine
def action(message, client, config):
    # Get configuration values
    forward_chan = config.get('Pokemon', 'forward_chan')
    forward_names = json.loads(config.get('Pokemon', 'forward_names'))
    production = config.getboolean('Pokemon', 'production')

    # if forward_from.lower() in str(message.author).lower() and len(message.embeds) > 0:
    if str(message.author).lower() in forward_names and len(message.embeds) > 0:

        # Parse the information
        json_blob = message.embeds[0]
        map_url = json_blob['url']
        map_image_url = json_blob['image']['url']

        try:
            # Parse the Title
            split_title = json_blob['title'].split()
            pokemon_name = split_title[0]
            pokemon_iv_percent = split_title[1]
            pokemon_cp = split_title[2]
            pokemon_level = split_title[3]
            pokemon_stats = split_title[4]

            # Parse Description - Make sure there are matches
            description = json_blob['description']

            alert_name = re.search("alert-.*", description)
            if alert_name:
                alert_name = alert_name.group(0)

            # Brute-force guess at location name, usually on the first line
            else:
                alert_name = description.split("\n")[0]

            moves = re.search("\[.*\]", description)
            if moves:
                moves = moves.group(0)

            spawn_time = re.search("\(.*", description)
            if spawn_time:
                spawn_time = spawn_time.group(0)

            fl_url = re.search("https:.*", description)
            if fl_url:
                fl_url = fl_url.group(0)

            # Get the Thumbnail URL
            pokemon_thumbnail_url = json_blob['thumbnail']['proxy_url']

            # Build the new Embed
            embed_title = pokemon_name + " - " + pokemon_iv_percent + " - " + pokemon_cp + " - [Maps Link]"
            pokemon_embed = Embed(title=embed_title, color=Color.green())
            pokemon_embed.add_field(name="Alert", value=alert_name, inline=True)
            pokemon_embed.add_field(name="Level", value=pokemon_level, inline=True)
            pokemon_embed.add_field(name="Moves", value=moves, inline=True)
            pokemon_embed.add_field(name="Stats", value=pokemon_stats, inline=True)
            pokemon_embed.add_field(name="Spawn Timer", value=spawn_time, inline=True)
            # pokemon_embed.add_field(name="FLPokeMap Link", value=fl_url, inline=True)
            pokemon_embed.set_thumbnail(url=pokemon_thumbnail_url)
            pokemon_embed.set_image(url=map_image_url)
            pokemon_embed.set_footer(text="Alerts provided by Florida PokeMap. For more information and to sign up for "
                                          "your own customized alert feed, visit https://flpokemap.com/")
            pokemon_embed.url = map_url

            # Wrap the Message Send action
            try:
                target_channel = discord.utils.get(client.get_all_channels(), name=forward_chan)
                target_role = discord.utils.get(target_channel.server.roles, name="rares")

                # Check if we're in quiet time
                now = datetime.datetime.utcnow()
                quiet_start = datetime.datetime(now.year, now.month, now.day, 5)
                quiet_end = datetime.datetime(now.year, now.month, now.day, 11)
                quiet_time = quiet_start < now < quiet_end

                # If we're configured for production, send to a discord server
                if production:
                    # Notification For 100% IV
                    if pokemon_iv_percent == '100%' and not quiet_time:
                        message_content = '<@&' + target_role.id + '>'
                        yield from client.send_message(target_channel, message_content)

                    yield from client.send_message(target_channel, embed=pokemon_embed)
                    # yield from client.send_message(message.author, embed=pokemon_embed)

                # Otherwise send to the configured test user
                else:
                    print("I'm not in production!")
                    for chan in client.private_channels:
                        target_user = discord.utils.get(chan.recipients, name="gradius")

                        if target_user is not None:
                            yield from client.send_message(target_user, embed=pokemon_embed)

            except:
                print("Failed to send message.")
                print(traceback.format_exc())

        except:
            print("Message parsing failed.")
            print(json_blob)
            print(traceback.format_exc())

