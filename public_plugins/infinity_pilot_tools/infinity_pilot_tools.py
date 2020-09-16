# TODO: report on users that aren't in the DB but in the discord
# TODO: automatically format people's Discord names
# TODO: add users to the DB when they're given a "member" role, but request that they send screenshots
# TODO: add users to a verified role once they've provided account screenshots and confirmed names

import csv
import logging
import traceback
from discord import Embed, Color
from libs.infinity_management import mgmt_db

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <infinity_pilot_tools.py> Tools for managing Pilot profiles.")

pilot_manager = mgmt_db.PilotManager()

help_str = """*Amos Pilot Tools - help*

```
!pt help - this message
!pt grant-member <ROLE_ID> <CHANNEL_ID> : grant the ROLE_ID to everyone in the CHANNEL_ID used
!pt create-pilots <ROLE_ID> : create pilot profiles for every member in the ROLE_ID
```
"""


async def action(**kwargs):
    """
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    split_message = message.content.split()
    admin_channel_id = config.getint('infinity', 'admin_channel_id')
    admin_id = config.getint('infinity', 'admin_id')
    guild = message.channel.guild

    if message.channel.id == admin_channel_id and message.author.id == admin_id:
        if len(split_message) > 0 and split_message[0] == '!pt':
            if len(split_message) == 2:
                if split_message[1] == 'filldb':
                    with open('pilots.csv') as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        for row in csv_reader:
                            try:
                                discord_id = int(row[0])
                                member = guild.get_member(discord_id)

                                if member:
                                    character_names = [n for n in row[2:] if n != '']
                                    pilot_manager.add_pilot(discord_id, member.name, member.discriminator, character_names=character_names)
                            except:
                                print("Unable to add member")
                                print(traceback.format_exc())

                    print("DB fill complete.")

                if split_message[1] == 'builddb':
                    pilot_manager.build_db()
                    print("DB build complete.")

                if split_message[1] == 'audit':
                    message_list = []
                    result_string = ""
                    missing_count = 0
                    target_channel = guild.get_channel(722851595519262733)
                    for member in target_channel.members:
                        if not member.bot:
                            pilot = pilot_manager.get_pilot(member.id)

                            if not pilot:
                                missing_count += 1
                                if len(result_string) >= 1900:
                                    message_list.append(result_string)
                                    result_string = f"{member.name}#{member.discriminator} - {[r.name for r in member.roles]}\n"
                                else:
                                    result_string += f"{member.name}#{member.discriminator} - {[r.name for r in member.roles]}\n"

                    await message.channel.send(
                        f"Out of {len(guild.members)} members, {missing_count} either haven't provided a profile screenshot or provided one that couldn't be processed.")

                    for outmsg in message_list:
                        await message.channel.send(f"```\n{outmsg}```")

                if split_message[1] == 'help':
                    await message.channel.send(help_str)

            if len(split_message) == 3:
                if split_message[1] == 'create-pilots':
                    target_role_id = int(split_message[2])
                    target_role = guild.get_role(target_role_id)

                    for member in target_role.members:
                        pilot_manager.add_pilot(member.id, member.name, member.discriminator, character_names=[])

            if len(split_message) == 4:
                if split_message[1] == 'grant-role':
                    target_channel_id = int(split_message[3])
                    target_channel = message.guild.get_channel(target_channel_id)
                    target_role_id = int(split_message[2])
                    target_role = guild.get_role(target_role_id)
                    user_count = 0

                    for user in target_channel.members:
                        if not user.bot:
                            user_count += 1
                            await user.add_roles(target_role, reason=f"[Amos BOT] - adding user via grant-member command from {target_role_id}.")

                    await message.channel.send(f"{user_count} users have been added to the role.")