# TODO: implement refresh and confirm logic from the public portion of the plugin


import logging
from libs.infinity_management import rfq_libs

logger = logging.getLogger('gradiusbot')
logger.info("[Reaction Plugin] <infinity_rfq.py>: Reaction portion of the Infinity RFQ plugin.")

emoji_dict = rfq_libs.emoji_dict


async def action(**kwargs):
    event_type = kwargs['event_type']
    client = kwargs['client']
    config = kwargs['config']

    if event_type == 'add':
        reaction = kwargs['reaction']
        reaction_sender = kwargs['user']
        message = reaction.message

        if reaction_sender != client.user:
            print(emoji_dict['refresh'] == str(reaction.emoji))
            if str(reaction.emoji) == emoji_dict['refresh']:
                print("refresh")
            if str(reaction.emoji) == emoji_dict['confirm']:
                print("confirm")
