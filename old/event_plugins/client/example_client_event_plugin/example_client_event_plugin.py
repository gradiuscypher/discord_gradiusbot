import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Client Event Plugin] <example_client_event_plugin.py>: This plugin shows you how to use member events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']

    if event_type == 'client.guild.join':
        guild = kwargs['guild']
        print("Client has joined the guild {}".format(guild))

    if event_type == 'client.guild.remove':
        guild = kwargs['guild']
        print("Client has been removed from the guild {}".format(guild))

    if event_type == 'client.guild.available':
        guild = kwargs['guild']
        print("Client guild {} is now available.".format(guild))

    if event_type == 'client.guild.unavailable':
        guild = kwargs['guild']
        print("Client guild {} is now unavailable.".format(guild))
