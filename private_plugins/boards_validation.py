import asyncio
import discord
from libs.custom_games.libs import members as members
from libs.server_management import ServerManagement


sm = ServerManagement()

print("[Private Plugin] <boards_validation.py>: This plugin allows users to validate their account manually.")

greeting = """
Welcome to the Boards Events Discord server! Here we use Summoner Name validation to ensure that everyone joining us has a valid summoner name.

To validate your summoner name, please visit this forum post here {} and post this randomized message: `{}`

Once this has been posted, our robots should get you put into the right Discord groups within a few minutes.

If you're having trouble, don't hesitate to PM a moderator on this server.
"""

return_greeting = """
Looks like you've been here before, thanks for coming back! If you've already posted your validation string, our helpful robots should be putting you in the right groups shortly.

To remind you, your validation string is: `{}` and you should post it in this thread here if you haven't already: {}
"""


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()

    if split_content[0] == '!validate':
        author = message.author
        validation_url = config.get('GeneralDiscussion', 'validation_post_url')
        not_validated_group_name = config.get("GeneralDiscussion", "not_validated_group")
        discord_name = (author.name + "#" + author.discriminator)
        default_server = sm.get_default_server(author.id)
        target_server = client.get_server(default_server)

        if target_server is None:
            yield from client.send_message(message.author, "Please set your default server ID with the `!servers` command before using this command.")

        else:
            # Returns a bool, random_string. bool tells if member has already started the validation process
            not_validated_role = discord.utils.get(target_server.roles, name=not_validated_group_name)
            validation = members.start_validation(author.id, discord_name)

            server = target_server
            target_user = server.get_member(message.author.id)

            if validation[0]:
                yield from client.add_roles(target_user, not_validated_role)
                yield from client.send_message(author, greeting.format(validation_url, validation[1]))
            else:
                yield from client.add_roles(target_user, not_validated_role)
                yield from client.send_message(author, return_greeting.format(validation[1], validation_url))
