import discord.utils
from discord.enums import ChannelType
from discord import Embed, Color
import libs.scripts.examples
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <example_script_plugin.py> An example of how plugins can run separate scripts.")


async def action(**kwargs):
    """
    :param kwargs:
    :return:
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    # ref: https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
    if message.content == 'run plugin':
        method = getattr(libs.scripts.examples, 'example_action_1')
        method()
