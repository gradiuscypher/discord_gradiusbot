import logging

logger = logging.getLogger('gradiusbot')
logger.info("[Reaction Plugin] <infinity_rfq.py>: Reaction portion of the Infinity RFQ plugin.")


async def action(**kwargs):
    event_type = kwargs['event_type']
    client = kwargs['client']
    config = kwargs['config']

    if event_type == 'add':
        reaction = kwargs['reaction']
        reaction_sender = kwargs['user']
        message = reaction.message
