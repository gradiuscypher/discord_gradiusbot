import asyncio
import discord
from libs import banpool

print("[Scheduled Task] <banpool_tasks.py>: Scheduled tasks for the banpool.")


@asyncio.coroutine
def action(client, config):
    while True:
        print("This is an example of a scheduled task being executed.")
        yield from asyncio.sleep(60)
