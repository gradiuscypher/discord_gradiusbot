"""
# TODO: Worflow:
* User starts a ticket with `!rfq start <ORDER_ID>`
* Opens up a channel with RFQ Admins and the user under the RFQ section
* Sends a control panel Embed and pins the embed to the channel for easy access
  * Embed includes all request information
"""
# TODO: update help

import logging
from discord import Embed, Color, utils, PermissionOverwrite
from libs.infinity_management import rfq_libs


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


async def action(**kwargs):
    """
    config values
    [infinity]
    rfq_ticket_category_id =
    rfq_admin_role_id =
    bot_role_id =
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    # configuration section
    rfq_ticket_category_id = config.getint('infinity', 'rfq_ticket_category_id')
    rfq_admin_role_id = config.getint('infinity', 'rfq_admin_role_id')
    bot_role_id = config.getint('infinity', 'bot_role_id')

    split_message = [s.lower() for s in message.content.split()]

    if len(split_message) == 2 and split_message[0] == '!rfq':
        if split_message[1] == 'help':
            await message.channel.send(help_str)

    if len(split_message) == 3 and split_message[0] == '!rfq':
        if split_message[1] == 'start':
            order_num = split_message[2]

            rfq_ticket_category = client.get_channel(rfq_ticket_category_id)
            target_guild = rfq_ticket_category.guild
            rfq_admin_role = target_guild.get_role(rfq_admin_role_id)
            bot_role = target_guild.get_role(bot_role_id)
            permissions = {
                target_guild.default_role: PermissionOverwrite(read_messages=False),
                rfq_admin_role: PermissionOverwrite(read_messages=True, send_messages=True),
                bot_role: PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, add_reactions=True, manage_channels=True),
                message.author: PermissionOverwrite(read_messages=True, send_messages=True)
            }
            ticket_channel = await rfq_ticket_category.create_text_channel(f'rfq-ticket-{order_num}', overwrites=permissions)

            # send message to channel with details
            title_str = f"RFQ Ticket - {order_num}"
            instruction_str = f"""Click {rfq_libs.emoji_dict['filled']} to confirm that the materials have been sent. This will notify the requester.

            Click {rfq_libs.emoji_dict['canceled']} to cancel this request. Either the requester or the admins can cancel this.

            Click {rfq_libs.emoji_dict['assign']} to assign this ticket to yourself. Click it again to unassign yourself.

            Click {rfq_libs.emoji_dict['close']} to close this ticket and delete this channel.

            The RFQ sheet can be found here: 
            https://docs.google.com/spreadsheets/d/1-vCG3AxO51-P7iGSkkfl24K77qvsgPwTD8VgFpCm33w/edit#gid=700379285
            """
            rfq_ticket = Embed(title=title_str, color=Color.green(), description=instruction_str)
            rfq_ticket.add_field(name="Requester", value=f"<@{message.author.id}>", inline=True)
            rfq_ticket.add_field(name="Order Number", value=f"{order_num}", inline=True)
            rfq_ticket.add_field(name="Assignee", value=f"None", inline=True)
            rfq_ticket_msg = await ticket_channel.send(embed=rfq_ticket)
            await rfq_ticket_msg.add_reaction(rfq_libs.emoji_dict['filled'])
            await rfq_ticket_msg.add_reaction(rfq_libs.emoji_dict['canceled'])
            await rfq_ticket_msg.add_reaction(rfq_libs.emoji_dict['close'])
            await rfq_ticket_msg.add_reaction(rfq_libs.emoji_dict['assign'])
            await rfq_ticket_msg.pin()

            # Send a ping message to alert everyone related to the ticket
            ping_message = f"<@&{rfq_admin_role_id}> <@{message.author.id}>\n\nSee message pins for a quick link to the Ticket Details."
            await ticket_channel.send(ping_message)

            # respond back to the requester with a message
            request_title = "RFQ Ticket Opened"
            request_channel = rfq_ticket_msg.jump_url
            request_description = f"""A ticket has been created with the RFQ admins.

            Please click this link to be sent to the ticket channel and give the RFQ admins any additional information.
            
            {request_channel}
            """
            request_response = Embed(title=request_title, color=Color.green(), description=request_description)
            await message.channel.send(embed=request_response)

