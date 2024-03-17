import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <example.py>: This plugin echoes details back to the sender.")


@asyncio.coroutine
def action(message, config):
    yield from message.channel.send("Your message: " + message.content)
    yield from message.channel.send("You are: " + message.author.name)
