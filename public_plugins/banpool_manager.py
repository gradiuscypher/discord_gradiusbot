import asyncio
import discord
from libs import banpool
from discord import Embed, Color

print("[Public Plugin] <banpool_manager.py>: This plugin manages the banpool.")

banpool_manager = banpool.BanPoolManager()

help_string = """
**BanPool Commands**
BanPool is a Discord bot that automatically coordinates bans between Discord servers which have the bot.
All commands start with `!bp`. Do not include the `<` or `>` brackets in your commands.

```
!bp help - this command

!bp list - list all available banpools. Currently only 'global' is used

!bp listusers <BANPOOL_NAME> - list all user IDs in the banpool

!bp adduser <BANPOOL_NAME> <USER_ID> - add user ID to the banpool

!bp adduserlist <BANPOOL_NAME> <USER_ID_LIST> - ban a list of user IDs, separated by commas

!bp listexception - list all of the ban exceptions: a user ID and Server ID pair

!bp addexception <USER_ID> <SERVER_ID> - add a ban exception pair for user ID and Server ID

!bp removeuser <BANPOOL_NAME> <USER_ID> - remove user ID from the banpool

!bp removeexception <USER_ID> <SERVER_ID> - remove a ban exception pair for user ID and Server ID

!bp isuserbanned <USER_ID> - check if the user ID is in any banpools

!bp getuserinfo <USER_ID> - check to see if the user ID is present in any servers
```
"""


def chunks(l, n):
    # Stolen from: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    for i in range(0, len(l), n):
        yield l[i:i + n]


@asyncio.coroutine
async def action(message, client, config):
    """
    Config Values:
    [banpool]
    # The Discord ID of the Admin user
    admin_server_id =
    admin_group =
    admin_chan =
    # the time to wait between executing scheduled tasks in seconds
    task_length =

    :param message: discord message obj
    :param client: discord client obj
    :param config: config obj
    :return:
    """

    # get config values
    admin_server_id = config.get('banpool', 'admin_server_id')
    admin_group = config.get('banpool', 'admin_group')
    admin_chan = config.get('banpool', 'admin_chan')

    server_id = message.server.id
    source_chan = message.channel.name

    in_admin_group = discord.utils.get(message.author.roles, name=admin_group)

    if server_id == admin_server_id and in_admin_group and source_chan == admin_chan:
        split_content = message.content.split()

        if split_content[0] == '!bp':

            if split_content[1] == 'help':
                await client.send_message(message.channel, help_string)

            if split_content[1] == 'list':
                banpool_list = banpool_manager.banpool_list()
                bp_embed = Embed(title="Active BanPools", color=Color.green())

                for bp in banpool_list:
                    bp_embed.add_field(name=bp.pool_name, value=bp.pool_description, inline=True)
                await client.send_message(message.channel, embed=bp_embed)

            if split_content[1] == 'listusers' and len(split_content) == 3:
                banpool_name = split_content[2]
                userlist = banpool_manager.banpool_user_list(banpool_name)

                ul_embed = Embed(title=banpool_name + " banned IDs", color=Color.green())

                if userlist:
                    # Split the list into chunks
                    user_chunks = chunks(userlist, 25)
                    for chunk in user_chunks:
                        field_string = ''
                        for user in chunk:
                            field_string += str(user.user_id) + "\n"
                        ul_embed.add_field(name="User IDs", value=field_string, inline=True)
                await client.send_message(message.channel, embed=ul_embed)

            if split_content[1] == 'adduser' and len(split_content) == 4:
                banpool_name = split_content[2]
                user_id = split_content[3]
                result = banpool_manager.add_user_to_banpool(banpool_name, user_id)

                if result[1]:
                    # The add was successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.green(), description=result[0])
                else:
                    # The add was not successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])

                await client.send_message(message.channel, embed=notice_embed)

            if split_content[1] == 'adduserlist' and len(split_content) == 4:
                banpool_name = split_content[2]
                user_id_list = split_content[3]

                result = banpool_manager.add_userlist_to_banpool(banpool_name, user_id_list)

                if result[1]:
                    # The add was successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.green(), description=result[0])
                else:
                    # The add was not successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])

                await client.send_message(message.channel, embed=notice_embed)

            if split_content[1] == 'listexception':
                exception_list = banpool_manager.exception_list()

                if len(exception_list) > 0:
                    el_embed = Embed(title="Exception List", color=Color.green())
                    user_string = ''
                    server_string = ''

                    for user in exception_list:
                        user_string += str(user.user_id) + "\n"
                        server_string += str(user.server_id) + "\n"

                    el_embed.add_field(name="User ID", value=user_string)
                    el_embed.add_field(name="Server ID", value=server_string)
                else:
                    el_embed = Embed(title="Exception List", color=Color.red(), description="There are no exceptions.")

                await client.send_message(message.channel, embed=el_embed)

            if split_content[1] == 'addexception' and len(split_content) == 4:
                user_id = split_content[2]
                server_id = split_content[3]

                result = banpool_manager.add_user_to_exceptions(user_id, server_id)

                if result[1]:
                    # The add was successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.green(), description=result[0])
                else:
                    # The add was not successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])
                await client.send_message(message.channel, embed=notice_embed)

            if split_content[1] == 'removeuser' and len(split_content) == 4:
                banpool_name = split_content[2]
                user_id = split_content[3]

                result = banpool_manager.remove_user_from_banpool(banpool_name, user_id)

                if result[1]:
                    # The add was successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.green(), description=result[0])
                else:
                    # The add was not successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])
                await client.send_message(message.channel, embed=notice_embed)

            if split_content[1] == 'removeexception' and len(split_content) == 4:
                user_id = split_content[2]
                server_id = split_content[3]

                result = banpool_manager.remove_user_from_exceptions(user_id, server_id)

                if result[1]:
                    # The add was successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.green(), description=result[0])
                else:
                    # The add was not successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])
                await client.send_message(message.channel, embed=notice_embed)

            if split_content[1] == 'isuserbanned' and len(split_content) == 3:
                user_id = split_content[2]
                result = banpool_manager.is_user_banned(user_id)

                if result[1]:
                    # The add was successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.green(),
                                         description='User is in banpool: ' + result[0])
                else:
                    # The add was not successful
                    notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])

                await client.send_message(message.channel, embed=notice_embed)

            if split_content[1] == 'getuserinfo' and len(split_content) == 3:
                user_id = split_content[2]
                found_user = False

                user_embed = Embed(title="Discord User", color=Color.green())
                user_embed.add_field(name="User ID", value=user_id, inline=False)
                server_name_string = ''
                user_object = None

                for server in client.servers:
                    user = server.get_member(user_id)

                    if user:
                        found_user = True
                        server_name_string += server.name + "\n"
                        user_object = user

                if found_user:
                    user_embed.add_field(name="In Servers", value=server_name_string)
                    user_embed.add_field(name="User Name", value=user_object.name + "#" + str(user_object.discriminator), inline=True)
                    user_embed.set_thumbnail(url=user_object.avatar_url)

                    await client.send_message(message.channel, embed=user_embed)
                else:
                    fail_embed = Embed(title="Discord User", color=Color.red(), description="User was not found on any of my servers.")
                    await client.send_message(message.channel, embed=fail_embed)
