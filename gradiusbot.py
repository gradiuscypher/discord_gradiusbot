#!/usr/bin/env python
"""
ref: https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html#using-cogs
ref: https://discordpy.readthedocs.io/en/stable/ext/commands/extensions.html
ref: https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#ext-commands-commands
ref: https://discordpy.readthedocs.io/en/stable/logging.html
ref: https://github.com/Rapptz/discord.py/blob/v1.7.2/examples/basic_bot.py
"""

import discord
import json
import logging
from configparser import RawConfigParser
from discord.ext import commands

# Setup Logging
logger = logging.getLogger('gradiusbot')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('gradiusbot.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

# setup intents
intents = discord.Intents.all()

# setup the config
config = RawConfigParser()
config.read('config.conf')
token = config.get('discord', 'token')
cog_list = json.loads(config.get('discord', 'cogs'))


# run the bot
if __name__ == '__main__':
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as <{bot.user.id}> {bot.user.name}")

    for cog_name in cog_list:
        bot.load_extension('cogs.' + cog_name)
        print(f"Loading {cog_name}")
    bot.run(token)