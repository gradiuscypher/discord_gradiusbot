import asyncio
import discord
import libs.custom_games.libs.members as memberslib

print("[Scheduled Task] <move_validated_users.py>: Moves validated users from 'not_validated' to 'member'.")

validation_message = """
I've now properly confirmed your validation message, thank you! You should now have access to the proper chat channels.

If you have any follow up questions, please message the mods.
"""


@asyncio.coroutine
def action(client, config):
    not_validated_group_name = config.get("GeneralDiscussion", "not_validated_group")
    validated_group_name = config.get("GeneralDiscussion", "validated_group")
    forum_location = config.get("GeneralDiscussion", "forum_location")
    forum_post = config.get("GeneralDiscussion", "forum_post")

    while True:
        # Grab the validation forums and check for new validations
        memberslib.check_for_validation(forum_location, forum_post)

        if client.is_logged_in:
            # Get the active server
            # TODO: This needs to be modified for multi-server implementations
            server = discord.utils.get(client.servers)

            # Get Roles objects
            not_validated_role = discord.utils.get(server.roles, name=not_validated_group_name)
            validated_role = discord.utils.get(server.roles, name=validated_group_name)

            # Check for users in the not_validated role
            # TODO: this function may balloon in cost as we get more members, need to watch this
            for member in server.members:
                if not_validated_role in member.roles:
                    # Check to see if the user has validated via the forums
                    validated = memberslib.is_user_validated(member.id)

                    # If they've validated via the Board forums
                    if validated:
                        yield from client.replace_roles(member, validated_role)
                        yield from client.send_message(member, validation_message)

        yield from asyncio.sleep(5)
