# TODO:
"""
Workflow:
    Owner creates queue with details
        name
        description
        duration
        number of users at a time
        dodo code
    User joins queue via reactions
        Two reactions to join and leave queue

Configuration:
    Which channel does it post to?

Notes:
    How do we handle editing?
    Do we want a multi-step setup, or all in one line?
    How long do we keep partially configured setups before removing them?
        Set a TTL on a queue object to expire after X minutes
"""

import asyncio
import logging
import traceback

logger = logging.getLogger('gradiusbot')
logger.info("[Private Plugin] <ac_queue.py>: Create and join queues for Animal Crossing activities.")

help_str = """
** User Control Panel **
```
!acq help - this message
```
"""

queue_list = []


@asyncio.coroutine
async def action(**kwargs):
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    split_content = message.content.split()

    if split_content[0] == '!acq':
        if split_content[1] == 'help':
            await message.channel.send(help_str)

        if split_content[1] == 'add':
            pass

        if split_content[1] == 'edit':
            pass

        if split_content[1] == 'remove':
            pass

        if split_content[1] == 'quit':
            pass
