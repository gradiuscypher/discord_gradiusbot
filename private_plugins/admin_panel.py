import asyncio
import logging
import discord
from discord import Embed, Color

print("[Private Plugin] <admin_panel.py>: This plugin lets you administer your bot.")

# Setup Logging
logger = logging.getLogger('banpool_admin_panel')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('banpool_admin.log')
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

        if split_content[0] == '!admin' and len(split_content) > 1:
            logger.info("{}#{} [{}] has attempted to execute command {}".format(
                message.author.name, message.author.discriminator, message.author.id, message.content))

            if split_content[1] == 'listservers':
                server_list = client.servers
                result_str = "```"

                for server in server_list:
                    result_str += server.name + "\n"
                result_str += "```"

                await client.send_message(message.channel, result_str)
