import asyncio
import logging
import discord
from discord import Embed, Color

print("[Private Plugin] <admin_panel.py>: This plugin lets you administer your bot.")

# Setup Logging
logger = logging.getLogger('banpool_manager')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('banpool.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


@asyncio.coroutine
async def action(message, client, config):
    admin_id = config.get('adminpanel', 'admin_id')

    if message.author.id == admin_id:
        split_content = message.content.split()

        if split_content[0] == '!admin':
            pass

        # await client.send_message(message.channel, "Your message: " + message.content)
