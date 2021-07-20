#!/usr/bin/env python
"""
ref: https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html#using-cogs
ref: https://discordpy.readthedocs.io/en/stable/ext/commands/extensions.html
ref: https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#ext-commands-commands
ref: https://discordpy.readthedocs.io/en/stable/logging.html
ref: https://github.com/Rapptz/discord.py/blob/v1.7.2/examples/basic_bot.py
"""

import discord
import logging
import os.path
import pickle
from discord.ext import commands
from config import token, cogs
from cogs.role_cta_button import RoleCtaView

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


# run the bot
if __name__ == '__main__':
    bot = commands.Bot(command_prefix='!', intents=intents)
    persistent_views_added = False

    @bot.event
    async def on_ready():
        global persistent_views_added
        print(f"Logged in as <{bot.user.id}> {bot.user.name}")

        if not persistent_views_added:
            # load the persistent role CTA messages from a pickle
            if os.path.exists('role_cta.pickle'):
                logger.info("Adding persistent role views...")
                with open('role_cta.pickle', 'rb') as cta_pickle:
                    target_roles = pickle.load(cta_pickle)
                for role_id in target_roles:
                    bot.add_view(RoleCtaView(role_id))

            persistent_views_added = True

    for cog_name in cogs:
        bot.load_extension('cogs.' + cog_name)
        print(f"Loading {cog_name}")
    bot.run(token)