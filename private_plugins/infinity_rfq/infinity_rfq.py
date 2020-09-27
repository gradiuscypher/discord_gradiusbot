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
!rfq start <ORDER_NUMBER> - start an RFQ material request. Please include your order number from the RFQ sheet.
```
"""

rfq_manager = rfq_libs.RfqManager()
rfq_sessions = {}

# airtable_obj = None


async def action(**kwargs):
    # global airtable_obj
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    # if not airtable_obj:
    #     airtable_basekey = config.get('infinity', 'airtable_basekey')
    #     airtable_tablename = config.get('infinity', 'airtable_tablename')
    #     airtable_apikey = config.get('infinity', 'airtable_apikey')
    #     airtable_obj = Airtable(airtable_basekey, airtable_tablename, airtable_apikey)

    split_message = [s.lower() for s in message.content.split()]

    airtable_url = config.get('infinity', 'airtable_url')

    if len(split_message) == 2 and split_message[0] == '!rfq':
        if split_message[1] == 'help':
            await message.channel.send(help_str)

    if len(split_message) == 3 and split_message[0] == '!rfq':
        if split_message[1] == 'start':
            order_num = split_message[2]
            rfq_embed = Embed(title="RFQ Material Request Open", color=Color.green(), description=f"A request ticket for Order # {order_num} has been sent to the Admins.")
            await message.channel.send(embed=rfq_embed)

            # Send the RFQ alert to the admin channel
            rfq_admin_channel_id = config.getint('infinity', 'rfq_admin_channel_id')
            rfq_admin_channel = client.get_channel(rfq_admin_channel_id)

            instruction_str = f"Click {rfq_libs.emoji_dict['confirm']} to confirm that the materials have been sent. This will notify the requester.\n\n" \
                              f"Click {rfq_libs.emoji_dict['close']} to mark the request as closed without sending materials. This will notify the requester."
            rfq_ticket = Embed(title="", color=Color.green(), description=instruction_str)
            rfq_ticket.add_field(name="Requester", value=f"<@{message.author.id}>", inline=True)
            rfq_ticket.add_field(name="Order Number", value=f"{order_num}", inline=True)
            rfq_ticket_msg = await rfq_admin_channel.send(embed=rfq_ticket)
            await rfq_ticket_msg.add_reaction(rfq_libs.emoji_dict['filled'])
            await rfq_ticket_msg.add_reaction(rfq_libs.emoji_dict['close'])

            # airtable_url = f"{airtable_url}{message.author.id}"
            # start_str = f"""**Infinity RFQ Tool - Getting Started**
            #
            # To get started, use this form to request the materials that you need for your current jobs:
            # <{airtable_url}>
            #
            # - Submit the form multiple times to request multiple materials.
            # - Use the {rfq_libs.emoji_dict['refresh']} reaction to update this RFQ.
            # - Use the {rfq_libs.emoji_dict['confirm']} reaction to submit the request to the RFQ admins
            # """
            # description_str = f"**Requested Materials**\n```\n```"
            # rfq_embed = Embed(title="RFQ - Open Request", color=Color.green(), description=description_str)
            #
            # await message.channel.send(cleandoc(start_str))
            # embed_msg = await message.channel.send(embed=rfq_embed)
            # await embed_msg.add_reaction(rfq_libs.emoji_dict['refresh'])
            # await embed_msg.add_reaction(rfq_libs.emoji_dict['confirm'])

            # add_rfq_session(message.author.id)
