import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Reaction Event Plugin] <example_reaction_event_plugin.py>: This plugin shows you how to use reaction events.")


@asyncio.coroutine
async def action(event_type, reaction, config, user=None):
    if event_type == 'add' and user:
        await reaction.message.channel.send("{} added a {} reaction to the message with ID {}".format(user.name, reaction.emoji, reaction.message.id))

    if event_type == 'remove' and user is not None:
        await reaction.message.channel.send("{} removed a {} reaction from the message with ID {}".format(user.name, reaction.emoji, reaction.message.id))

    if event_type == 'clear':
        await reaction.message.channel.send("A bulk reaction clear event happened. Fancy that.")
