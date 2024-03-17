import traceback
import asyncio
import discord
import logging
import json

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <project_rogue.py>: Experimental user management functionality.")
target_users = json.loads(open('target_users.json').read())


@asyncio.coroutine
async def action(**kwargs):
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    if len(message.content) > 1:
        # validate owner
        owner_ids = json.loads(config.get('project_rogue', 'owner_list'))

        if message.author.id in owner_ids:
            # split the message command
            split_message = message.content.split()

            # validate message is project_rogue command
            if split_message[0] == '!pr':
                # check to see if any banlist users are in the server
                if split_message[1] == 'checkusers':
                    ban_json = json.loads(open('valid_bans.json').read())

                    await message.channel.send(f"Checking {len(ban_json)} users to see if they're in the server.")

                    for user in ban_json:
                        user_exists = message.guild.get_member(user)

                        if user_exists:
                            await message.channel.send(f"[WARN] `{user_exists.display_name}#{user_exists.discriminator}` is in the server and will be banned!")

                    await message.channel.send("Completed current user check.")

                # validate the users on the json list
                if split_message[1] == 'validateusers':
                    await message.channel.send(f"Executing ban on {len(target_users)} users.")

                    with open('valid_bans.json', 'w') as valid_bans:
                        ban_list = []
                        count = 1

                        for user_id in target_users:
                            try:
                                target_member = await client.get_user_info(user_id)

                                if 'Deleted User' in target_member.display_name:
                                    await message.channel.send(f"[DELETED] {target_member.display_name}#{target_member.discriminator}")

                                else:
                                    await message.channel.send(f"[{count}/{len(target_users)}] {target_member.display_name}#{target_member.discriminator}")
                                    ban_list.append(user_id)
                            except:
                                await message.channel.send(f"Failed to ban {user_id}:\n```\n{traceback.format_exc()}\n```")
                            count += 1

                        valid_bans.write(json.dumps(ban_list))

                # ban the users on the banlist
                if split_message[1] == 'banusers':
                    ban_json = json.loads(open('valid_bans.json').read())
                    await message.channel.send(f"Adding {len(ban_json)} members to the ban list.")

                    for user in ban_json:
                        try:
                            target_member = await client.get_user_info(user)
                            await message.guild.ban(target_member, reason="[BANNED BY BOT]")
                        except:
                            await message.channel.send(f"Failed to ban {user_id}:\n```\n{traceback.format_exc()}\n```")

                    await message.channel.send(f"Completed banning users.")
