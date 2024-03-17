import asyncio
import logging
import traceback

logger = logging.getLogger('gradiusbot')
logger.info("[Public Plugin] <eve_pi.py>: Monitor and track EVE PI.")

help_str = """
** User Control Panel **
```
!ucp help - this message
```
"""


@asyncio.coroutine
async def action(**kwargs):
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    try:
        split_content = message.content.split()

        # main section of the user control panel
        if split_content[0] == '!ucp':
            if len(split_content) == 2:
                if split_content[1] == 'help':
                    await message.channel.send(help_str)

            if len(split_content) == 3:
                # namecolor commands
                if split_content[1] == 'color':
                    # explain how to use the command and list available colors
                    if split_content[2] == 'help':
                        print(message.server.roles)
                    if split_content[2] == 'set':
                        pass

    except:
        print(traceback.format_exc())
