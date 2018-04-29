import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Private Event Plugin] <example_private_event_plugin.py>: This plugin shows you how to use private events.")


@asyncio.coroutine
async def action(event_type, channel, config, after=None):
    if event_type == 'create':
        print("Private channel was created:\n\n{}".format(channel))
    if event_type == 'delete':
        print("Private channel was deleted:\n\n{}".format(channel))
    if event_type == 'update' and after:
        print("Private channel was updated:\n\nbefore:{}\n\nafter:{}".format(channel, after))
    if event_type == 'pin_update':
        print("Private channel had pin update:\n\nchannel:{}\n\nlast pin date:{}".format(channel, after))

