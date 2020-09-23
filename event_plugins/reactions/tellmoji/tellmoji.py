import logging
from libs.tellmoji_libs import TellmojiMatch

logger = logging.getLogger('gradiusbot')
logger.info("[Reaction Plugin] <tellmoji.py>: Reaction portion of the Tellmoji plugin.")

tellmoji_matches = {}


async def action(**kwargs):
    event_type = kwargs['event_type']
    client = kwargs['client']
    config = kwargs['config']

    if event_type == 'add':
        reaction = kwargs['reaction']
        reaction_sender = kwargs['user']
        message = reaction.message

        # double check that the message sent was sent by our bot
        if message.author == client.user:
            challenge_target = reaction.message.mentions[0]
            if "Tellmoji match" in message.content and reaction_sender == challenge_target:
                if str(reaction.emoji) == '👍':
                    # create a TellmojiMatch keyed off the authors Discord ID. That way an author can only have one match at a time.
                    await message.channel.send("Challenge accepted!")
                elif str(reaction.emoji) == '👎':
                    await message.delete()
