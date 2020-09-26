# TODO: turn data into ticket, remove data from airtable when request is filled
# TODO: change these to reactions
# TODO: include request ID, requester name

import logging
from airtable import Airtable
from discord import Embed, Color, utils
from libs.infinity_management import rfq_libs
from inspect import cleandoc


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
            - Use the `!rfq update` command to update this RFQ.
            - Use the `!rfq submit` to submit the request to the RFQ admins
            """
            description_str = f"**Requested Materials**\n```\n```"
            rfq_embed = Embed(title="RFQ - Open Request", color=Color.green(), description=description_str)

            await message.channel.send(cleandoc(start_str))
            embed_msg = await message.channel.send(embed=rfq_embed)

            rfq_sessions[message.author.id] = {
                'materials': {},
                'embed_id': embed_msg.id
            }

        if split_message[1] == 'update':
            if message.author.id not in rfq_sessions.keys():
                await message.channel.send("Please start an RFQ session with `!rfq start`.")

            else:
                rfq_session = rfq_sessions[message.author.id]
                new_materials = rfq_libs.update_rfq_order(message.author.id, airtable_obj)

                for material in new_materials:
                    if material in rfq_session['materials'].keys():
                        rfq_session['materials'][material] += new_materials[material]
                    else:
                        rfq_session['materials'][material] = new_materials[material]

                embed_id = rfq_session['embed_id']
                materials_str = ""

                for material in rfq_session['materials']:
                    materials_str += f"{material} : {rfq_session['materials'][material]}\n"

                description_str = f"**Requested Materials**\n```{materials_str}\n```"
                rfq_embed = Embed(title="RFQ - Open Request", color=Color.green(), description=description_str)
                target_message = await message.channel.fetch_message(embed_id)
                await target_message.delete()
                new_message = await message.channel.send(embed=rfq_embed)
                rfq_session['embed_id'] = new_message.id

        if split_message[1] == 'submit':
            pass
