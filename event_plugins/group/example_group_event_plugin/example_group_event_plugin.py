import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Group Event Plugin] <example_group_event_plugin.py>: This plugin shows you how to use group events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']

    if event_type == 'group.join':
        channel = kwargs['channel']
        user = kwargs['user']
        print("Joined a group channel {} with the user {}".format(channel, user))
    if event_type == 'group.join':
        channel = kwargs['channel']
        user = kwargs['user']
        print("Removed a group channel {} with the user {}".format(channel, user))

