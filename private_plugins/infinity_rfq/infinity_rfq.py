# TODO: turn data into ticket, remove data from airtable when request is filled
# TODO: change these to reactions
# TODO: include request ID, requester name

import logging
from airtable import Airtable
from discord import Embed, Color, utils
from inspect import cleandoc
from libs.infinity_management import rfq_libs
from event_plugins.reactions.infinity_rfq.infinity_rfq import add_rfq_session


logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <infinity_rfq.py>: Submit RFQ requests via PM.")


help_str = """
** Ininity RFQ Tool**
```
!rfq help - this command
!rfq start - start an RFQ material request. This will provide you a unique link to your RFQ form. To request multiple items, just refresh the form page.
!rfq update - update the current RFQ ticket to see the current amounts
!rfq submit - submit your RFQ request to be filled
```
"""

rfq_manager = rfq_libs.RfqManager()
rfq_sessions = {}

airtable_obj = None


async def action(**kwargs):
    global airtable_obj
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    if not airtable_obj:
        airtable_basekey = config.get('infinity', 'airtable_basekey')
        airtable_tablename = config.get('infinity', 'airtable_tablename')
        airtable_apikey = config.get('infinity', 'airtable_apikey')
        airtable_obj = Airtable(airtable_basekey, airtable_tablename, airtable_apikey)

    split_message = message.content.split()

    airtable_url = config.get('infinity', 'airtable_url')

    if len(split_message) == 2 and split_message[0] == '!rfq':
        if split_message[1] == 'help':
            await message.channel.send(help_str)

        if split_message[1] == 'start':
            airtable_url = f"{airtable_url}{message.author.id}"
            start_str = f"""**Infinity RFQ Tool - Getting Started**

            To get started, use this form to request the materials that you need for your current jobs:
            <{airtable_url}>

            - Submit the form multiple times to request multiple materials. 
            - Use the {rfq_libs.emoji_dict['refresh']} reaction to update this RFQ.
            - Use the {rfq_libs.emoji_dict['confirm']} reaction to submit the request to the RFQ admins
            """
            description_str = f"**Requested Materials**\n```\n```"
            rfq_embed = Embed(title="RFQ - Open Request", color=Color.green(), description=description_str)

            await message.channel.send(cleandoc(start_str))
            embed_msg = await message.channel.send(embed=rfq_embed)
            await embed_msg.add_reaction(rfq_libs.emoji_dict['refresh'])
            await embed_msg.add_reaction(rfq_libs.emoji_dict['confirm'])

            add_rfq_session(message.author.id)

        if split_message[1] == 'submit':
            pass
