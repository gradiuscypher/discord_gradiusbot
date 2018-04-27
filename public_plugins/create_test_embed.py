import discord
import asyncio
from discord import Embed, Color

print("[Public Plugin] <create_test_embed.py>: This plugin creates embeds.")


@asyncio.coroutine
def action(message, client, config):
    print(message.content)
    if message.content == "!embeds":
        embed_channel_name = config.get("Tournament", "embed_channel")
        embed_channel = discord.utils.get(client.get_all_channels(), name=embed_channel_name)

        if embed_channel:
            test_embed = Embed(title="Test Embed Title", color=Color.dark_magenta())
            test_embed.add_field(name="Value1", value="VALUE1", inline=True)
            test_embed.add_field(name="Value1", value="VALUE1", inline=True)
            test_embed.add_field(name="Value1", value="VALUE1", inline=True)
            test_embed.add_field(name="Value1", value="VALUE1", inline=True)

            yield from client.send_message(embed_channel, embed=test_embed)
