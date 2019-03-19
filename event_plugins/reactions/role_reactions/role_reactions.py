import asyncio
import logging
import json
import traceback
import discord.utils
from discord import Emoji, PartialEmoji
from pathlib import Path

"""
Config options

[role_reactions]
role_json = event_plugins/reactions/role_reactions/testroles.json
temp_filename = event_plugins/reactions/role_reactions/roles_msg_id.tmp
"""


logger = logging.getLogger('gradiusbot')
logger.info("[Public Plugin] <role_reactions.py>: This allows users to change their roles via Message Reactions.")


def load_json_config(config_location='event_plugins/reactions/role_reactions/roles.json'):
    # Load the roles from JSON
    with open(config_location, encoding='utf-8') as roles_file:
        return json.load(roles_file)


def write_temp_message_id(message_id, temp_filename):
    with open(temp_filename, 'w') as temp_id_file:
        temp_id_file.write(message_id)


def get_temp_message_id(temp_filename):
    tmp_file = Path(temp_filename)

    if tmp_file.exists():
        with open(temp_filename, 'r') as temp_id_file:
            return int(temp_id_file.read())
    else:
        return None


def build_assign_message(guild, roles_json):
    available_roles = roles_json['available_roles']
    message_string = ""

    for role in available_roles:
        emoji = discord.utils.get(guild.emojis, name=role)
        message_string += f"{emoji} - `{roles_json['role_descriptions'][role]}`\n"

    return message_string


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']
    client = kwargs['client']
    config = kwargs['config']

    try:
        role_filename = config.get('role_reactions', 'role_json')
        temp_filename = config.get('role_reactions', 'temp_filename')
        roles_json = load_json_config(config_location=role_filename)

    except:
        print(traceback.format_exc())
        temp_filename = 'roles_msg_id.tmp'
        roles_json = load_json_config()

    available_roles = roles_json['available_roles']

    if event_type == 'raw_add':
        payload = kwargs['payload']

        # Used to set up or resend reaction message
        if isinstance(payload.emoji, PartialEmoji) and payload.emoji.name == roles_json['role_setup_emoji'] and payload.user_id == roles_json['admin_id']:
            send_chan = client.get_channel(id=roles_json['role_assign_channel_id'])
            assign_message_id = get_temp_message_id(temp_filename)

            # delete the previous config message if it exists
            if assign_message_id:
                target_message = await send_chan.get_message(assign_message_id)
                await target_message.delete()

            # Build the role assign message
            assign_message = await send_chan.send(build_assign_message(send_chan.guild, roles_json))

            for role in available_roles:
                emoji = discord.utils.get(assign_message.guild.emojis, name=role)
                await assign_message.add_reaction(emoji)

            # write the new message id to tmp
            write_temp_message_id(str(assign_message.id), temp_filename)

        # All other user actions
        if isinstance(payload.emoji, PartialEmoji) and payload.message_id == get_temp_message_id(temp_filename):
            guild = discord.utils.get(client.guilds, id=payload.guild_id)
            user = guild.get_member(payload.user_id)

            if payload.emoji.name in roles_json['available_roles'].keys():
                # get the role object
                role = discord.utils.get(guild.roles, name=available_roles[payload.emoji.name])

                # try to add the role
                await user.add_roles(role)

    if event_type == 'raw_remove':
        payload = kwargs['payload']

        if isinstance(payload.emoji, PartialEmoji) and payload.message_id == get_temp_message_id(temp_filename):
            guild = discord.utils.get(client.guilds, id=payload.guild_id)
            user = guild.get_member(payload.user_id)

            if payload.emoji.name in roles_json['available_roles'].keys():
                # get the role object
                role = discord.utils.get(guild.roles, name=available_roles[payload.emoji.name])

                # try to add the role
                await user.remove_roles(role)

