import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <echo.py>: This plugin echoes stuff to a public channel.")


@asyncio.coroutine
async def action(**kwargs):
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    if len(message.content) > 0:
        await message.channel.send(message.content)
