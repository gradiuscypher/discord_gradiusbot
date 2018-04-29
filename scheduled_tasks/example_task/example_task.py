import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Scheduled Task] <example_task.py>: This is a scheduled background task.")


@asyncio.coroutine
def action(client, config):
    while True:
        if client.is_ready():
            print("This is an example of a scheduled task being executed.")
            print("I am {}.".format(client.user))
            print("I belong to the guilds: {}".format(client.guilds))
            print("I can see the users: {}".format(client.users))
            print()
        yield from asyncio.sleep(5)
