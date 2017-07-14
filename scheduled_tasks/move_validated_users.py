import asyncio
import discord

print("[Scheduled Task] <move_validated_users.py>: Moves validated users from 'not_validated' to 'member'.")


@asyncio.coroutine
def action(client, config):
    not_validated_group_name = config.get("GeneralDiscussion", "not_validated_group")
    validated_group_name = config.get("GeneralDiscussion", "validated_group")

    while True:
        if client.is_logged_in:
            # Get the active server
            # TODO: This needs to be modified for multi-server implementations
            server = discord.utils.get(client.servers)

            # Check for users in the not_validated role
            # TODO: this function may balloon in cost as we get more members, need to watch this
            not_validated = discord.utils.get(server.roles, name=not_validated_group_name)
            for member in server.members:
                if not_validated in member.roles:
                    # Check to see if the user has validated via the forums
                    pass

            # Check to see if their discord name exists in the gdusers database and is validated to a summoner name
            # If validated, remove the not_validated role and move to member role
        yield from asyncio.sleep(5)
