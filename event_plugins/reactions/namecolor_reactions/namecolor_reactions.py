import asyncio
import logging
import json
import discord.utils
from discord import Emoji, PartialEmoji
from pathlib import Path

logger = logging.getLogger('gradiusbot')
logger.info("[Public Plugin] <namecolor_reactions.py>: This allows users to change their namecolor via Message Reactions.")


def load_json_config():
    # Load the roles from JSON
    with open('event_plugins/reactions/namecolor_reactions/namecolors.json', encoding='utf-8') as roles_file:
        return json.load(roles_file)


def write_temp_message_id(message_id):
    with open('namecolor_msg_id.tmp', 'w') as temp_id_file:
        temp_id_file.write(message_id)


def get_temp_message_id():
    tmp_file = Path('namecolor_msg_id.tmp')

    if tmp_file.exists():
        with open('namecolor_msg_id.tmp', 'r') as temp_id_file:
            return int(temp_id_file.read())
    else:
        return None


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']
    client = kwargs['client']
    namecolor_json = load_json_config()

    if event_type == 'raw_add':
        payload = kwargs['payload']

        # check if the reaction is the configuration emoji along with "config-namecolor" as the message from admin
        # if so, generate a new message with all available namecolor_* roles
        if payload.user_id == namecolor_json['admin_id'] and payload.channel_id == namecolor_json['role_assign_channel_id']:
            payload_message = await ((client.get_channel(payload.channel_id)).get_message(payload.message_id))

            if payload_message.content == 'config-namecolor':
                guild = client.get_guild(payload.guild_id)
                roles = guild.roles
                namecolor_roles = []

                for r in roles:
                    if 'namecolor_' in r.name:
                        namecolor_roles.append(r)

        # otherwise check if the reaction is a valid namecolor reaction and add as needed

    if event_type == 'raw_remove':
        payload = kwargs['payload']

        # check if the reaction is a valid namecolor and remove as needed
