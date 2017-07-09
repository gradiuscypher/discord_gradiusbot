import asyncio
import random
import string

print("[Event Plugin] <boards_greeting.py>: This plugin greets users and tells them how to validate their account.")

greeting = """
Welcome to the Boards Events Discord server! Here we use Summoner Name validation to ensure that everyone joining us has a valid summoner name.

To validate your summoner name, please visit this forum post here {} and post this randomized message: `{}`

Once this has been posted, reply to this message with !validate and a direct link to your post. You can find your post's direct link by INSTRUCTIONS_HERE.

For example a correct reply to this would be: 
`!validate INSERT_EXAMPLE_VALIDATION_LINK_HERE`

If you're having trouble, don't hesitate to PM a moderator on this server.
"""


@asyncio.coroutine
def action(event_object, client, config, event_type, object_after=None):
    validation_url = config.get('GeneralDiscussion', 'validation_post_url')
    random_message = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

    if event_type == "member_join":
        yield from client.send_message(event_object, greeting.format(validation_url, random_message))
