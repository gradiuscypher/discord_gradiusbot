import asyncio
import discord
import json
import logging
import re
import traceback
import discord.errors
from discord import Embed, Color

from libs import banpool, banpool_configuration


# Setup the BanPoolManager
banpool_manager = banpool.BanPoolManager()

# Setup the BanpoolConfiguration
banpool_config = banpool_configuration.BanpoolConfigManager()

# Setup Logging
logger = logging.getLogger('gradiusbot')
logger.info("[Public Plugin] <banpool_manager.py>: This plugin manages the banpool.")

help_string = """
**BanPool Commands**
BanPool is a Discord bot that automatically coordinates bans between Discord servers which have the bot.
All commands start with `!bp`. Do not include the `<` or `>` brackets in your commands.

```
!bp help - this command

!bp list - list all available banpools. Currently only 'global' is used

!bp addpool <POOL_NAME> <POOL_DESCRIPTION> - add a new banpool to the pool list

!bp listusers <BANPOOL_NAME> - list all user IDs in the banpool

!bp adduser <BANPOOL_NAME> <USER_ID> <REASON> - add user ID to the banpool. REASON is a description of why the user was banpooled.

!bp adduserlist <BANPOOL_NAME> <USER_ID_LIST> - ban a list of user IDs, separated by commas

!bp listexception - list all of the ban exceptions: a user ID and Server ID pair

!bp addexception <USER_ID> <SERVER_ID> - add a ban exception pair for user ID and Server ID

!bp removepool <BANPOOL_NAME> - delete the banpool and unsubscribe all servers

!bp removeuser <BANPOOL_NAME> <USER_ID> - remove user ID from the banpool

!bp removeexception <USER_ID> <SERVER_ID> - remove a ban exception pair for user ID and Server ID

!bp isuserbanned <USER_ID> - check if the user ID is in any banpools

!bp getuserinfo <USER_ID> - check to see if the user ID is present in any servers

!bp whatservers - list what servers the bot is in

!bp serversmissing - list what servers the bot is not in, based on the CommunityMains invite channel
```
"""


def chunks(l, n):
    # Stolen from: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    for i in range(0, len(l), n):
        yield l[i:i + n]

# Setup Config
try:
    with open('conf/config.json') as json_file:
        config_json = json.loads(json_file.read())
except:
    print(traceback.format_exc())


async def action(**kwargs):
    message = kwargs['message']
    client = kwargs['client']

    """
    Config Values:
    [banpool]
    # The Discord ID of the Admin user
    admin_server_id =
    admin_group =
    admin_chan =
    # the time to wait between executing scheduled tasks in seconds
    task_length =
    # community server where to get Server invites from
    community_server_id =
    community_server_chan_id = 

    :param message: discord message obj
    :param config: config obj
    :return:
    """

    # get config values
    admin_server_id = config_json['banpool']['admin_server_id']
    admin_group = config_json['banpool']['admin_group']
    admin_chan = config_json['banpool']['admin_chan']
    community_server_id = config_json['banpool']['community_server_id']
    community_server_chan_id = config_json['banpool']['community_server_chan_id']

    server_id = message.guild.id
    source_chan = message.channel.name
    channel = message.channel

    try:
        if server_id == admin_server_id and source_chan == admin_chan:
            in_admin_group = discord.utils.get(message.author.roles, name=admin_group)

            if in_admin_group:
                split_content = message.content.split()

                if split_content[0] == '!bp' and len(split_content) > 1:
                    if split_content[1] == 'help':
                        await channel.send(help_string)

                    if split_content[1] == 'list':
                        # TODO: list the pools in one column and include pool description and count
                        banpool_list = banpool_manager.banpool_list()
                        bp_embed = Embed(title="Active BanPools", color=Color.green())

                        for bp in banpool_list:
                            bp_embed.add_field(name=bp.pool_name, value=bp.pool_description, inline=False)
                        await channel.send(embed=bp_embed)

                    if split_content[1] == 'addpool' and len(split_content) >= 4:
                        pool_name = split_content[2]
                        pool_description = ' '.join(split_content[3:])
                        result = banpool_manager.create_banpool(pool_name, pool_description)

                        if result[1]:
                            notice_embed = Embed(title="BanPool Manager", color=Color.green(),
                                                 description=result[0])
                        else:
                            # The add was not successful
                            notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])

                        await message.channel.send(embed=notice_embed)

                    if split_content[1] == 'removepool' and len(split_content) == 3:
                        pool_name = split_content[2]
                        delete_success = banpool_manager.delete_banpool(pool_name)

                        if delete_success:
                            banpool_config.banpool_is_deleted(pool_name)

                            notice_text = "Banpool removal was successful."
                            notice_embed = Embed(title="BanPool Manager", color=Color.green(),
                                                 description=notice_text)
                        else:
                            notice_text = "Banpool removal was not successful."
                            notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=notice_text)

                        await message.channel.send(embed=notice_embed)

                    if split_content[1] == 'listusers' and len(split_content) == 3:
                        banpool_name = split_content[2]
                        userlist = banpool_manager.banpool_user_list(banpool_name)

                        if userlist:
                            userlist_len = str(len(userlist))
                            # Split the list into chunks
                            user_chunks = chunks(userlist, 1)
                            total_users = 0

                            while user_chunks:
                                try:
                                    message_string = ''
                                    while len(message_string) <= 1900:
                                        user = next(user_chunks)[0]
                                        message_string += str(user.user_id) + ' '
                                        total_users += 1
                                    message_string += '```'
                                    message_header = '**Banned Users (Users: {}/{})**\n```\n'.format(total_users, userlist_len)
                                    await channel.send(message_header + message_string)
                                except StopIteration:
                                    message_string += '```'
                                    message_header = '**Banned Users (Users: {}/{})**\n```\n'.format(total_users, userlist_len)
                                    await channel.send(message_header + message_string)
                                    break

                    if split_content[1] == 'adduser' and len(split_content) > 4:
                        banpool_name = split_content[2]
                        user_id = split_content[3]
                        target_user = client.get_user(int(user_id))
                        reason = ' '.join(split_content[4:])
                        result = banpool_manager.add_user_to_banpool(banpool_name, user_id, reason)
                        if result[1]:
                            # The add was successful
                            notice_embed = Embed(title="BanPool Manager - User Added", color=Color.green(), description=result[0])
                            if target_user:
                                notice_embed.add_field(name="User Name",
                                                    value=target_user.name + "#" + str(target_user.discriminator),
                                                    inline=False)
                            notice_embed.add_field(name="User ID", value=user_id, inline=True)
                            notice_embed.add_field(name="Banpool Name", value=banpool_name, inline=False)
                            notice_embed.add_field(name="Ban Reason", value=reason, inline=False)
                        else:
                            # The add was not successful
                            notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])

                        await channel.send(embed=notice_embed)

                    if split_content[1] == 'adduserlist' and len(split_content) == 4:
                        banpool_name = split_content[2]
                        user_id_list = split_content[3]

                        result = banpool_manager.add_userlist_to_banpool(banpool_name, user_id_list, "Userlist Import")

                        if result[1]:
                            # The add was successful
                            notice_embed = Embed(title="BanPool Manager", color=Color.green(), description=result[0])
                        else:
                            # The add was not successful
                            notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])

                        await channel.send(embed=notice_embed)

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

                        await channel.send(embed=el_embed)

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
                        await channel.send(embed=notice_embed)

                    if split_content[1] == 'removeuser' and len(split_content) == 4:
                        banpool_name = split_content[2]
                        user_id = split_content[3]

                        result = banpool_manager.remove_user_from_banpool(banpool_name, user_id)

                        if result[1]:
                            # The add was successful
                            notice_embed = Embed(title="BanPool Manager", color=Color.green(), description=result[0])
                            notice_embed.add_field(name="User ID", value=user_id, inline=True)
                            notice_embed.add_field(name="Banpool Name", value=banpool_name, inline=False)
                        else:
                            # The add was not successful
                            notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])
                        await channel.send(embed=notice_embed)

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
                        await channel.send(embed=notice_embed)

                    if split_content[1] == 'isuserbanned' and len(split_content) == 3:
                        user_id = split_content[2]
                        result = banpool_manager.is_user_banned(user_id)

                        if result[1]:
                            banpool_list = [p for p in result[0]]
                            ban_reasons = []

                            for p in banpool_list:
                                ban_reasons.append(result[0][p].reason)

                            notice_embed = Embed(title="BanPool Manager", color=Color.green(), description='User is in banpools: `' + str(banpool_list) + '`')
                            notice_embed.add_field(name="User ID", value=user_id, inline=True)
                            notice_embed.add_field(name="Ban Reason", value=str(ban_reasons), inline=False)
                        else:
                            # The add was not successful
                            notice_embed = Embed(title="BanPool Manager", color=Color.red(), description=result[0])

                        await channel.send(embed=notice_embed)

                    if split_content[1] == 'getuserinfo' and len(split_content) == 3:
                        user_id = split_content[2]
                        found_user = False

                        user_embed = Embed(title="Discord User", color=Color.green())
                        user_embed.add_field(name="User ID", value=user_id, inline=False)
                        server_name_string = ''
                        user_object = None

                        for server in client.guilds:
                            user = server.get_member(int(user_id))

                            if user:
                                found_user = True
                                server_name_string += server.name + "\n"
                                user_object = user

                        if found_user:
                            user_embed.add_field(name="In Servers", value=server_name_string)
                            user_embed.add_field(name="User Name", value=user_object.name + "#" + str(user_object.discriminator), inline=True)
                            user_embed.set_thumbnail(url=user_object.avatar_url)

                            await channel.send(embed=user_embed)
                        else:
                            fail_embed = Embed(title="Discord User", color=Color.red(), description="User was not found on any of my servers.")
                            await channel.send(embed=fail_embed)

                    if split_content[1] == 'whatservers' and len(split_content) == 2:
                        server_list = client.guilds
                        result_str = "```\n"

                        for server in server_list:
                            result_str += server.name + "\n"
                        result_str += "```"

                        await channel.send(result_str)

                    if split_content[1] == 'serversmissing' and len(split_content) == 2:
                        community_server = client.get_guild(community_server_id)
                        community_chan = community_server.get_channel(community_server_chan_id)
                        result_string = '**Servers without Tim**\n```'
                        invalid_links = '**Invalid Invite Links**\n```'

                        await channel.send("Processing invite list, please wait ...")

                        async for hist_message in community_chan.history(limit=500):

                            for invite in re.findall(r"https?://discord.gg/\w*", hist_message.content):
                                try:
                                    found_invite = await client.get_invite(invite)

                                    if found_invite.guild not in client.guilds:
                                        result_string += found_invite.guild.name + "\n"
                                except discord.errors.NotFound:
                                    logger.debug('Unable to find a valid invite with this invite: {}'.format(invite))
                                    reformatted_link = invite.replace('.', '[.]')
                                    invalid_links += "{}".format(reformatted_link) + "\n"
                                    continue

                        result_string += '```'
                        invalid_links += '```'
                        await channel.send(result_string)
                        await channel.send(invalid_links)
    except:
        logger.error(traceback.format_exc())
