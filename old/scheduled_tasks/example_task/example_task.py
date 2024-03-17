import asyncio
import logging
from discord.ext.tasks import loop

logger = logging.getLogger('gradiusbot')

logger.info("[Scheduled Task] <example_task.py>: This is a scheduled background task.")


async def action(client, config):
    @loop(seconds=5)
    async def example_task():
        print(client.user)
        print("This is an example task.")

    @example_task.before_loop
    async def before_example():
        print("waiting for user to log in...")
        await client.wait_until_ready()

    example_task.start()
