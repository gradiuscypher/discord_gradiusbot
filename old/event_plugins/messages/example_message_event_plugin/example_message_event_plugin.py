import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Message Event Plugin] <example_message_event_plugin.py>: This plugin shows you how to use message events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']

    if event_type == 'delete':
        message = kwargs['message']
        await message.channel.send("You deleted: {}".format(message.content))

    if event_type == 'edit':
        before = kwargs['before']
        after = kwargs['after']
        await before.channel.send("You edited a message.\n\n Before it was :```{}```\n\n Now it's: ```{}```".format(before.content, after.content))
