import asyncio
import logging
import discord
import operator
import re
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

            if split_content[1] == 'usercount':
                result_embed = Embed(title="", color=Color.green())
                servers = client.servers
                result_dict = {}
                result_embed.description = "**Total Servers: **" + str(len(servers))
                server_names = ""
                server_counts = ""
                total_users = 0

                for server in servers:
                    result_dict[server.name] = len(server.members)

                sorted_val = sorted(result_dict.items(), key=operator.itemgetter(1))

                for i in sorted_val:
                    server_names += i[0] + "\n"
                    server_counts += str(i[1]) + "\n"
                    total_users += i[1]

                result_embed.description += "  **Total Users: **" + str(total_users)
                result_embed.add_field(name="User Count", value=server_counts)
                result_embed.add_field(name="Servers", value=server_names)

                await client.send_message(message.channel, embed=result_embed)

            if split_content[1] == 'missingservers' and len(split_content) == 2:
                community_server = client.get_server('125440014904590336')
                community_chan = community_server.get_channel('324969552452780042')
                result_string = '**Servers without Tim**\n```'

                await client.send_message(message.channel, "Processing invite list, please wait ...")

                async for hist_message in client.logs_from(community_chan, limit=500):

                    for invite in re.findall(r"https?://discord.gg/\w*", hist_message.content):
                        found_invite = await client.get_invite(invite)

                        if found_invite.server not in client.servers:
                            result_string += found_invite.server.name + "\n"

                result_string += '```'
                await client.send_message(message.channel, result_string)

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
