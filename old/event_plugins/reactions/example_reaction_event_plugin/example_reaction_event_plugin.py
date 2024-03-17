import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Reaction Event Plugin] <example_reaction_event_plugin.py>: This plugin shows you how to use reaction events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']

    if event_type == 'add':
        reaction = kwargs['reaction']
        user = kwargs['user']
        await reaction.message.channel.send("{} added a {} reaction to the message with ID {}".format(user.name, reaction.emoji, reaction.message.id))

    if event_type == 'remove':
        reaction = kwargs['reaction']
        user = kwargs['user']
        await reaction.message.channel.send("{} removed a {} reaction from the message with ID {}".format(user.name, reaction.emoji, reaction.message.id))

    if event_type == 'clear':
        message = kwargs['message']
        reactions = kwargs['reactions']
        await message.channel.send("{} had its reaction list removed:{}".format(message.id, reactions))

