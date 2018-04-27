import discord
import asyncio

print("[Public Plugin] <participation_role.py>: This plugin grants a role to those who speak in chat.")

help_message = """
    No interaction with this plugin available.
"""

# Cache of already evaluated users
user_id_cache = []


@asyncio.coroutine
async def action(message, client, config):
    """
    Config Values:
    [ParticipationRole]
    # The role that you want to assign to those who participate
    role_id =

    :param message: discord message obj
    :param client: discord client obj
    :param config: config obj
    :return:
    """
    author_id = message.author.id
    target_role_id = config.get("ParticipationRole", "role_id")
    target_role = discord.utils.get(message.server.roles, id=target_role_id)

    # For each message, check to see if the user id is part of the cached users list, ignore if true
    if author_id not in user_id_cache and len(message.content) > 0:
        # Try to get the target role from the author, if None, they don't have it assigned.
        # Make sure they only have 1 role to prevent cluttering roles on other tagged members
        if discord.utils.get(message.author.roles, id=target_role_id) is None and len(message.author.roles) <= 1:
            # Add the role to the user and add them to the cache
            await client.add_roles(message.author, target_role)
            await client.add_reaction(message, '👍')
            user_id_cache.append(author_id)
        else:
            # Add user to cache to avoid checking later
            user_id_cache.append(author_id)
