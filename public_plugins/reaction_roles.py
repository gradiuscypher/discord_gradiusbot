import discord
import asyncio

print("[Public Plugin] <reaction_roles.py>: This plugin gives users roles based on the reaction Emojis they click.")

help_message = """
    No interaction with this plugin available.
"""


@asyncio.coroutine
async def action(message, client, config):
    """
    Config Values:
    [reaction_roles]


    :param message: discord message obj
    :param client: discord client obj
    :param config: config obj
    :return:
    """
