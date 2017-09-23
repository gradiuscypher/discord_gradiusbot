import asyncio
import discord
from lol_customs import members


print("[Event Plugin] <boards_greeting.py>: This plugin greets users and tells them how to validate their account.")

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
def action(event_object, client, config, event_type, object_after=None):

    if event_type == "member_join":
        validation_url = config.get('GeneralDiscussion', 'validation_post_url')
        not_validated_group_name = config.get("GeneralDiscussion", "not_validated_group")
        discord_name = (event_object.name + "#" + event_object.discriminator)
        server = event_object.server
        not_validated_role = discord.utils.get(server.roles, name=not_validated_group_name)

        # Returns a bool, random_string. bool tells if member has already started the validation process
        validation = members.start_validation(event_object.id, discord_name)

        if validation[0]:
            yield from client.add_roles(event_object, not_validated_role)
            yield from client.send_message(event_object, greeting.format(validation_url, validation[1]))
        else:
            yield from client.add_roles(event_object, not_validated_role)
            yield from client.send_message(event_object, return_greeting.format(validation[1], validation_url))

