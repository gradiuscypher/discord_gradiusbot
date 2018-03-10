import discord
import asyncio
import json
import random
from discord import Embed, Color
from libs import emoji_list

print("[Public Plugin] <reaction_roles.py>: This plugin gives users roles based on the reaction Emojis they click.")

help_message = """
    No interaction with this plugin available.
"""


def get_available_roles(server, role_prepend_list):
    """
    Returns a list of roles available for people to select
    :param role_prepend_list: list of strings to look for in role names to allow assigning
    :return: list of Discord Roles
    """
    available_roles = []

    for r in server.roles:
        split_name = r.name.split('_')

        # Check to see if the first part of the role is in the prepend list
        if split_name[0] in role_prepend_list:
            available_roles.append(r)

    return available_roles


def update_roles(server, role_prepends):
    available_roles = get_available_roles(server, role_prepends)
    available_emojis = random.sample(emoji_list.alphanum, len(available_roles))
    role_dict = {}

    # build the role to emoji translation dictionary
    for role in available_roles:
        role_dict[role.name] = available_emojis.pop(), role

    role_list1 = available_roles[:len(available_roles)//2]
    role_list2 = available_roles[len(available_roles)//2:]

    role_names1 = '\n'.join([role_dict[x.name][0] + " : " + x.name for x in role_list1])
    role_names2 = '\n'.join([role_dict[x.name][0] + " : " + x.name for x in role_list2])

    role_embed = Embed(title="Available Roles", color=Color.green())
    role_embed.add_field(name="----", value=role_names1, inline=True)
    role_embed.add_field(name="----", value=role_names2, inline=True)

    return role_embed, role_dict


@asyncio.coroutine
async def action(message, client, config):
    """
    Config Values:
    [reaction_roles]
    role_prepends = ["prepend1", "prepend2"]


    :param message: discord message obj
    :param client: discord client obj
    :param config: config obj
    :return:
    """
    author_id = message.author.id
    role_dict = None
    role_prepends = json.loads(config.get('reaction_roles', 'role_prepends'))

    if message.content == '!update':
        # target_role_id = config.get("ParticipationRole", "role_id")
        # target_role = discord.utils.get(message.server.roles, id=target_role_id)

        role_embed, role_dict = update_roles(message.server, role_prepends)
        sent_message = await client.send_message(message.channel, embed=role_embed)

        for role in role_dict:
            await client.add_reaction(sent_message, role_dict[role][0])

    if message.content == "!emoji":
        emoji = random.choice(emoji_list.all_emoji)
        await client.add_reaction(message, emoji)

