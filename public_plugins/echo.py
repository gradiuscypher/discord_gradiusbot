import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <echo.py>: This plugin echoes stuff to a public channel.")


@asyncio.coroutine
async def action(message, config):
    await message.channel.send(message.content)
