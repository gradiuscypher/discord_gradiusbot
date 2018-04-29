import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Message Event Plugin] <example_message_event_plugin.py>: This plugin shows you how to use message events.")


@asyncio.coroutine
async def action(event_type, message, config, after=None):
    if event_type == 'delete':
        await message.channel.send("You deleted: {}".format(message.content))

    if event_type == 'edit':
        if after:
            await message.channel.send("You edited a message.\n\n Before it was :```{}```\n\n Now it's: ```{}```".format(message.content, after.content))
