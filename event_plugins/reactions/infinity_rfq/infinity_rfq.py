# TODO: create transcript
# TODO: state will not carry over if bot is restarted with open tickets


import logging
from discord import Embed, Color
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

        # config values
        rfq_admin_role_id = config.getint('infinity', 'rfq_admin_role_id')

        # useful objects
        message = reaction.message
        guild = message.guild
        rfq_admin_role = guild.get_role(rfq_admin_role_id)

        if reaction_sender != client.user:
            if str(reaction.emoji) == emoji_dict['filled'] and rfq_admin_role in reaction_sender.roles:
                await request_filled(guild, message, rfq_admin_role_id)
            if str(reaction.emoji) == emoji_dict['close'] and rfq_admin_role in reaction_sender.roles:
                await request_closed(message)
            if str(reaction.emoji) == emoji_dict['canceled']:
                await request_canceled(guild, message, rfq_admin_role_id)
            if str(reaction.emoji) == emoji_dict['assign']:
                await request_assigned(reaction, reaction_sender, message)

    elif event_type == 'remove':
        reaction = kwargs['reaction']
        reaction_sender = kwargs['user']

        # useful objects
        message = reaction.message

        if str(reaction.emoji) == emoji_dict['assign']:
            await request_assigned(reaction, reaction_sender, message, reaction_add=False)


async def request_filled(guild, message, rfq_admin_role_id):
    # alert the requester
    requester_id = int(message.embeds[0].fields[0].value.split('@')[1].replace('>', ''))
    request_id = message.embeds[0].fields[1].value
    requester = guild.get_member(requester_id)
    msg_embed = Embed(title=f'RFQ {request_id} has been filled', description=f"An admin has filled your request - {request_id}", color=Color.green())
    await requester.send(embed=msg_embed)

    # tell the admin to close the ticket
    filled_msg = f"<@&{rfq_admin_role_id}>: This request has been filled. Please click {rfq_libs.emoji_dict['close']} to archive and close this channel."
    await message.channel.send(filled_msg)


async def request_canceled(guild, message, rfq_admin_role_id):
    # alert the requester
    requester_id = int(message.embeds[0].fields[0].value.split('@')[1].replace('>', ''))
    requester = guild.get_member(requester_id)
    request_id = message.embeds[0].fields[1].value
    msg_embed = Embed(title=f'RFQ {request_id} has been canceled', description=f"Someone has canceled your request - {request_id}", color=Color.red())
    await requester.send(embed=msg_embed)

    # tell the admin to close the ticket
    filled_msg = f"<@&{rfq_admin_role_id}>: This request has been canceled. Please click {rfq_libs.emoji_dict['close']} to archive and close this channel."
    await message.channel.send(filled_msg)

    # clear reactions and re-add the close reaction
    await message.clear_reactions()
    await message.add_reaction(rfq_libs.emoji_dict['close'])


async def request_closed(message):
    # create a transcript
    # TODO: create transcript

    # delete the channel
    await message.channel.delete()


async def request_assigned(reaction, reaction_sender, message, reaction_add=True):
    # check if it was an add or remove
    if reaction_add:
        if reaction.count == 2:
            # add/remove an assigned field to the embed
            new_embed = message.embeds[0].set_field_at(index=2, name="Assignee", value=f"<@{reaction_sender.id}>", inline=True)
            await message.edit(embed=new_embed)

            # add/remove the assigned emoji to the name
            await message.channel.edit(name=rfq_libs.emoji_dict['assign'] + ' ' + message.channel.name)
    else:
        # make sure the assignee is the one sending the remove reaction
        guild = message.guild
        assignee_id = int(message.embeds[0].fields[2].value.split('@')[1].replace('>', ''))
        assignee = guild.get_member(assignee_id)

        if assignee == reaction_sender:
            # add/remove an assigned field to the embed
            new_embed = message.embeds[0].set_field_at(index=2, name="Assignee", value=f"None", inline=True)
            await message.edit(embed=new_embed)

            # add/remove the assigned emoji to the name
            await message.channel.edit(name=message.channel.name[2:])
