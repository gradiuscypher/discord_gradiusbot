import asyncio
import discord
from libs import banpool
from discord import Embed, Color

print("[Public Plugin] <banpool_manager.py>: This plugin manages the banpool.")

banpool_manager = banpool.BanPoolManager()


@asyncio.coroutine
async def action(message, client, config):
    """
    Config Values:
    [banpool]
    # The Discord ID of the Admin user
    admin_server_id =
    admin_group =

    :param message: discord message obj
    :param client: discord client obj
    :param config: config obj
    :return:
    """

    # get config values
    admin_server_id = config.get('banpool', 'admin_server_id')
    admin_group = config.get('banpool', 'admin_group')

    server_id = message.server.id

    in_admin_group = discord.utils.get(message.author.roles, name=admin_group)

    if server_id == admin_server_id and in_admin_group:
        split_content = message.content.split()

        if split_content[0] == '!banpool':
            if split_content[1] == 'list':
                banpool_list = banpool_manager.banpool_list()
                bp_embed = Embed(title="Active BanPools", color=Color.green())

                for bp in banpool_list:
                    bp_embed.add_field(name=bp.pool_name, value=bp.pool_description, inline=True)
                await client.send_message(message.channel, embed=bp_embed)

            if split_content[1] == 'listusers':
                pass
            if split_content[1] == 'adduser':
                pass
            if split_content[1] == 'adduserlist':
                pass
            if split_content[1] == 'listexception':
                pass
            if split_content[1] == 'addexception':
                pass
            if split_content[1] == 'removeuser':
                pass
            if split_content[1] == 'removeexception':
                pass
