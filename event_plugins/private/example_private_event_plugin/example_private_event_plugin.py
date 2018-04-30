import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Private Event Plugin] <example_private_event_plugin.py>: This plugin shows you how to use private events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']

    if event_type == 'create':
        channel = kwargs['channel']
        print("Private channel was created:\n\n{}".format(channel))

    if event_type == 'delete':
        channel = kwargs['channel']
        print("Private channel was deleted:\n\n{}".format(channel))

    if event_type == 'update':
        before = kwargs['before']
        after = kwargs['after']
        print("Private channel was updated:\n\nbefore:{}\n\nafter:{}".format(before, after))

    if event_type == 'pin.update':
        channel = kwargs['channel']
        last_pin = kwargs['last_pin']
        print("Private channel had pin update:\n\nchannel:{}\n\nlast pin date:{}".format(channel, last_pin))

