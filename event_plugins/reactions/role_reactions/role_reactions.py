import asyncio
import logging
import json
import discord.utils
from discord import Emoji
from pathlib import Path


def load_json_config():
    # Load the roles from JSON
    with open('event_plugins/reactions/role_reactions/roles.json', encoding='utf-8') as roles_file:
        return json.load(roles_file)


def write_temp_message_id(message_id):
    with open('roles_msg_id.tmp', 'w') as temp_id_file:
        temp_id_file.write(message_id)


def get_temp_message_id():
    tmp_file = Path('roles_msg_id.tmp')

    if tmp_file.exists():
        with open('roles_msg_id.tmp', 'r') as temp_id_file:
            return temp_id_file.read()
    else:
        return None


def build_assign_message(guild):
    roles_json = load_json_config()
    available_roles = roles_json['available_roles']
    message_string = ""

    for role in available_roles:
        emoji = discord.utils.get(guild.emojis, name=role)
        message_string += f"{emoji} - `{roles_json['role_descriptions'][role]}`\n"

    return message_string


logger = logging.getLogger('gradiusbot')
logger.info("[Public Plugin] <role_reactions.py>: This allows users to change their roles via Message Reactions.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']
    reaction = kwargs['reaction']
    client = kwargs['client']
    user = kwargs['user']
    roles_json = load_json_config()
    available_roles = roles_json['available_roles']

    # Used to set up or resend reaction message
    if event_type == 'add' and isinstance(reaction.emoji, Emoji) and reaction.emoji.name == roles_json['role_setup_emoji'] and user.id == roles_json['admin_id']:
        send_chan = client.get_channel(id=roles_json['role_assign_channel_id'])
        assign_message_id = get_temp_message_id()

        # delete the previous config message if it exists
        if assign_message_id:
            target_message = await send_chan.get_message(assign_message_id)
            await target_message.delete()

        # Build the role assign message
        assign_message = await send_chan.send(build_assign_message(send_chan.guild))

        for role in available_roles:
            emoji = discord.utils.get(assign_message.guild.emojis, name=role)
            await assign_message.add_reaction(emoji)

        # write the new message id to tmp
        write_temp_message_id(str(assign_message.id))

    # All other user actions
    if event_type == 'add' and isinstance(reaction.emoji, Emoji):
        user = kwargs['user']
        guild = reaction.message.guild

        if reaction.emoji.name in roles_json['available_roles'].keys():
            # get the role object
            role = discord.utils.get(guild.roles, name=available_roles[reaction.emoji.name])

            # try to add the role
            await user.add_roles(role)

    if event_type == 'remove' and isinstance(reaction.emoji, Emoji):
        user = kwargs['user']
        guild = reaction.message.guild

        if reaction.emoji.name in roles_json['available_roles'].keys():
            # get the role object
            role = discord.utils.get(guild.roles, name=available_roles[reaction.emoji.name])

            # try to add the role
            await user.remove_roles(role)

