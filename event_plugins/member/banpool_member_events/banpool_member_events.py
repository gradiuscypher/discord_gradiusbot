import asyncio
import discord
import logging
import traceback
from libs import banpool
from discord import Embed, Color

print("[Event Plugin] <banpool_events.py>: This plugin manages banpool related events.")

banpool_manager = banpool.BanPoolManager()

# Setup Logging
logger = logging.getLogger('banpool_manager')
logger.setLevel(logging.DEBUG)


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']
    config = kwargs['config']
