import asyncio
import discord
from libs import banpool
from discord import Embed, Color

print("[Scheduled Task] <banpool_tasks.py>: Scheduled tasks for the banpool.")

banpool_manager = banpool.BanPoolManager()


@asyncio.coroutine
async def action(client, config):
    admin_server_id = config.get('banpool', 'admin_server_id')
    admin_chan_name = config.get('banpool', 'admin_chan')
    task_length = config.getint('banpool', 'task_length')
    admin_chan = None

    setting_up = True
    while setting_up:
        print("Waiting for client to log in...")
        if client.is_logged_in:
            # Setup Admin Messaging
            admin_server = discord.utils.get(client.servers, id=admin_server_id)
            admin_chan = discord.utils.get(admin_server.channels, name=admin_chan_name)
            setting_up = False
        await asyncio.sleep(5)

    while True:
        if client.is_logged_in:
            # Check each server for a user with a matching User ID and ban those found

            # Build a list of all banned user IDs
            banned_user_ids = []
            banpool_list = banpool_manager.banpool_list()

            for pool in banpool_list:
                userlist = banpool_manager.banpool_user_list(pool.pool_name)

                if userlist:
                    for user in userlist:
                        banned_user_ids.append(user.user_id)

            # Iterate through each server, looking for banned user IDs
            for server in client.servers:
                for user_id in banned_user_ids:
                    user = server.get_member(str(user_id))

                    # If a user was found, check to see if there's an exception. If not, ban them.
                    if user:
                        is_exception = banpool_manager.is_user_in_exceptions(user_id, server.id)

                        if not is_exception:
                            ban_embed = Embed(title="User Banned via Task", color=Color.green())
                            ban_embed.add_field(name="Server ID", value=server.id, inline=True)
                            ban_embed.add_field(name="User ID", value=user_id, inline=True)
                            ban_embed.add_field(name="User Name", value=user.name + "#" + str(user.discriminator), inline=True)
                            ban_embed.set_thumbnail(url=user.avatar_url)
                            ban_embed.set_footer(icon_url=server.icon_url, text=server.name)

                            await client.ban(user)
                            await client.send_message(admin_chan, embed=ban_embed)

        await asyncio.sleep(task_length)
