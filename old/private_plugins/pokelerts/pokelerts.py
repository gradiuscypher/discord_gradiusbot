"""
ref: https://github.com/gradiuscypher/discord_gradiusbot/blob/face4ca6654b3f98c9ad33f323ecac74a36cce9e/old/private_plugins/pokelerts.py
"""
import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <pokelerts.py>: This plugin manages alerts for Pokemon Go.")


@asyncio.coroutine
async def action(**kwargs):
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']
