import asyncio
import logging
import discord
import operator
import re
from discord import Embed, Color

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


logger.info("[Private Plugin] <admin_panel.py>: This plugin lets you administer your bot.")


@asyncio.coroutine
async def action(message, client, config):
    admin_id = config.getint('adminpanel', 'admin_id')

    if message.author.id == admin_id and len(message.content) > 0:
        split_content = message.content.split()

        if split_content[0] == '!admin' and len(split_content) > 1:
            community_server_id = config.getint('banpool', 'community_server_id')
            community_server_chan_id = config.getint('banpool', 'community_server_chan_id')

            logger.info("{}#{} [{}] has attempted to execute command {}".format(
                message.author.name, message.author.discriminator, message.author.id, message.content))

            if split_content[1] == 'listservers':
                server_list = client.guilds
                result_str = "```\n"

                for server in server_list:
                    result_str += server.name + "\n"
                result_str += "```"

                await message.channel.send(result_str)

            if split_content[1] == 'usercount':
                result_embed = Embed(title="", color=Color.green())
                guilds = client.guilds
                result_dict = {}
                result_embed.description = "**Total Servers: **" + str(len(guilds))
                server_names = ""
                server_counts = ""
                total_users = 0

                for guild in guilds:
                    result_dict[guild.name] = len(guild.members)

                sorted_val = sorted(result_dict.items(), key=operator.itemgetter(1))

                for i in sorted_val:
                    server_names += i[0] + "\n"
                    server_counts += str(i[1]) + "\n"
                    total_users += i[1]

                result_embed.description += "  **Total Users: **" + str(total_users)
                result_embed.add_field(name="User Count", value=server_counts)
                result_embed.add_field(name="Servers", value=server_names)

                await message.channel.send(embed=result_embed)

            if split_content[1] == 'missingservers' and len(split_content) == 2:
                community_server = client.get_guild(community_server_id)
                community_chan = community_server.get_channel(community_server_chan_id)
                result_string = '**Servers without Tim**\n```'
                invalid_links = '**Invalid Invite Links**\n```'

                await message.channel.send("Processing invite list, please wait ...")

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
                await message.channel.send(result_string)
                await message.channel.send(invalid_links)

            if split_content[1] == 'getuserinfo' and len(split_content) == 3:
                user_id = split_content[2]
                found_user = False

                user_embed = Embed(title="Discord User", color=Color.green())
                user_embed.add_field(name="User ID", value=user_id, inline=False)
                server_name_string = ''
                user_object = None

                for guild in client.guilds:
                    user = guild.get_member(int(user_id))

                    if user:
                        found_user = True
                        server_name_string += guild.name + "\n"
                        user_object = user

                if found_user:
                    user_embed.add_field(name="In Servers", value=server_name_string)
                    user_embed.add_field(name="User Name", value=user_object.name + "#" + str(user_object.discriminator), inline=True)
                    user_embed.set_thumbnail(url=user_object.avatar_url)

                    await message.channel.send(embed=user_embed)
                else:
                    fail_embed = Embed(title="Discord User", color=Color.red(), description="User was not found on any of my servers.")
                    await message.channel.send(embed=fail_embed)
