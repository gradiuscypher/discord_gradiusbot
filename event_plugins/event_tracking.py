import asyncio
import discord.utils
from discord import Embed
from discord import Color

print("[Event Plugin] <event_tracking.py>: This plugin tracks events and does things with them.")


@asyncio.coroutine
def action(event_object, client, config, event_type, object_after=None):

    alert_channel_name = config.get("BotSettings", "alert_channel")

    # Get the alert channel the bot was configured for
    alert_channel = discord.utils.get(client.get_all_channels(), name=alert_channel_name)

    if event_type == "member_join":

        # Send a message using a discord Embed object rather than plaintext message, it's fancier
        embed_object = Embed(title="Member Join", color=Color.green())

        # Check to see if the user has an avatar, if so use it as the Embed thumbnail
        if event_object.avatar_url != "":
            embed_object.set_thumbnail(url=event_object.avatar_url)

        # Add two embed fields with username and ID info. Inline so they create two columns on one line
        embed_object.add_field(name="Username", value="{}#{}".format(event_object.name, event_object.discriminator), inline=True)
        embed_object.add_field(name="ID", value=event_object.id, inline=True)

        yield from client.send_message(alert_channel, embed=embed_object)

    if event_type == "member_remove":
        embed_object = Embed(title="Member Leave", color=Color.red())
        if event_object.avatar_url != "":
            embed_object.set_thumbnail(url=event_object.avatar_url)
        embed_object.add_field(name="Username", value="{}#{}".format(event_object.name, event_object.discriminator), inline=True)
        embed_object.add_field(name="ID", value=event_object.id, inline=True)

        yield from client.send_message(alert_channel, embed=embed_object)

