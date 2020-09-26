# TODO: implement refresh and confirm logic from the public portion of the plugin
# TODO: can we remove a reaction in a DM?
# TODO: case insensitive


import logging
from airtable import Airtable
from discord import Embed, Color
from libs.infinity_management import rfq_libs

logger = logging.getLogger('gradiusbot')
logger.info("[Reaction Plugin] <infinity_rfq.py>: Reaction portion of the Infinity RFQ plugin.")

emoji_dict = rfq_libs.emoji_dict

rfq_sessions = {}
airtable_obj = None


async def action(**kwargs):
    global airtable_obj

    global rfq_sessions
    event_type = kwargs['event_type']
    client = kwargs['client']
    config = kwargs['config']

    if not airtable_obj:
        airtable_basekey = config.get('infinity', 'airtable_basekey')
        airtable_tablename = config.get('infinity', 'airtable_tablename')
        airtable_apikey = config.get('infinity', 'airtable_apikey')
        airtable_obj = Airtable(airtable_basekey, airtable_tablename, airtable_apikey)

    if event_type == 'add':
        reaction = kwargs['reaction']
        reaction_sender = kwargs['user']
        message = reaction.message

        if reaction_sender != client.user:
            if str(reaction.emoji) == emoji_dict['refresh']:
                await update_rfq_message(reaction_sender, reaction, reaction_sender.id, airtable_obj)
            if str(reaction.emoji) == emoji_dict['confirm']:
                print("confirm")


def add_rfq_session(userid):
    global rfq_sessions
    rfq_sessions = {
        userid: {}
    }


async def update_rfq_message(user, reaction, author_id, airtable):
    global rfq_sessions
    rfq_session = rfq_sessions[author_id]
    new_materials = rfq_libs.update_rfq_order(author_id, airtable)
    message = reaction.message

    for material in new_materials:
        if material in rfq_session.keys():
            rfq_session[material] += new_materials[material]
        else:
            rfq_session[material] = new_materials[material]

    materials_str = ""

    for material in rfq_session:
        materials_str += f"{material} : {rfq_session[material]}\n"

    description_str = f"**Requested Materials**\n```{materials_str}\n```"
    rfq_embed = Embed(title="RFQ - Open Request", color=Color.green(), description=description_str)
    target_message = await message.channel.fetch_message(message.id)
    # await reaction.remove(user)
    await target_message.edit(embed=rfq_embed)


async def confirm_rfq():
    pass
