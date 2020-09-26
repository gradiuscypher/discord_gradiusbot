# !rfq need - requests materials and starts count dialog, creates a ticket in the rfq admin chan
# !rfq close <TICKET ID> - closes the request ticket and reports to closure to requester
# save the logs of this ticket as part of the ticket embed, including time open, mats requested, etc

"""
configuration settings
[infinity]
"""

import logging
from discord import Embed, Color

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <infinity_rfq.py> Public portions of the Infinity RFQ bot.")


async def action(**kwargs):
    """
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    split_message = message.content.split()

    if len(split_message) == 2 and split_message[0] == '!rfq':
        if split_message[1] == 'need':
            pass

        if split_message[1] == 'close':
            pass
