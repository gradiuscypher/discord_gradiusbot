import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Scheduled Task] <example_task.py>: This is a scheduled background task.")


@asyncio.coroutine
async def action(client, config):
    while True:
        if client.is_ready():
            pass
        await asyncio.sleep(5)
