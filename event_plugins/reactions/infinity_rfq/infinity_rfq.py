# TODO: implement refresh and confirm logic from the public portion of the plugin


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
                await confirm_rfq(reaction_sender, reaction, config, client)
            if str(reaction.emoji) == emoji_dict['filled']:
                await request_filled(reaction, reaction_sender)
            if str(reaction.emoji) == emoji_dict['close']:
                await request_canceled(reaction, reaction_sender)


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
    await target_message.delete()
    embed_msg = await user.send(embed=rfq_embed)
    await embed_msg.add_reaction(rfq_libs.emoji_dict['refresh'])
    await embed_msg.add_reaction(rfq_libs.emoji_dict['confirm'])


async def confirm_rfq(user, reaction, config, client):
    global rfq_sessions
    message = reaction.message
    rfq_admin_channel_id = config.getint('infinity', 'rfq_admin_channel_id')
    rfq_admin_channel = client.get_channel(rfq_admin_channel_id)
    rfq_session = rfq_sessions[user.id]
    confirm_embed = Embed(title="RFQ Submitted", description="Thank you for submitting your RFQ. An admin will fill the request as soon as possible.", color=Color.green())
    await user.send(embed=confirm_embed)
    await message.delete()
    materials_str = ""

    for material in rfq_session:
        materials_str += f"{material} : {rfq_session[material]}\n"

    instruction_str = f"Click {rfq_libs.emoji_dict['confirm']} to confirm that the materials have been sent. This will notify the requester.\n" \
                      f"Click {rfq_libs.emoji_dict['close']} to mark the request as closed without sending materials. This will notify the requester.\n\n"
    description_str = instruction_str + f"**Requested Materials**\n```{materials_str}\n```"
    rfq_ticket = Embed(title='RFQ - Request Opened', color=Color.green(), description=description_str)
    rfq_ticket.add_field(name="Requester", value=f"<@{user.id}>")
    rfq_ticket_msg = await rfq_admin_channel.send(embed=rfq_ticket)
    await rfq_ticket_msg.add_reaction(rfq_libs.emoji_dict['filled'])
    await rfq_ticket_msg.add_reaction(rfq_libs.emoji_dict['close'])


async def request_canceled(reaction, user):
    message = reaction.message
    guild = message.guild
    embed = message.embeds[0]
    requester = guild.get_member(int(embed.fields[0].value.split('@')[1].replace('>', '')))
    msg_embed = Embed(title='RFQ has been canceled', description="An admin has canceled your request. Please speak with the RFQ admins for more information.", color=Color.red())
    await requester.send(embed=msg_embed)
    await message.clear_reactions()


async def request_filled(reaction, user):
    message = reaction.message
    embed = message.embeds[0]
    guild = message.guild
    requester = guild.get_member(int(embed.fields[0].value.split('@')[1].replace('>', '')))
    msg_embed = Embed(title='RFQ has been filled', description="An admin has filled your request.", color=Color.green())
    await requester.send(embed=msg_embed)
    await message.clear_reactions()
