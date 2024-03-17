import asyncio
import logging
from discord import utils
from discord import Embed, Color

logger = logging.getLogger('gradiusbot')

logger.info("[Member Event Plugin] <spotify_tracking.py>: This plugin monitors Spotify events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']
    before = kwargs['before']
    after = kwargs['after']

    if event_type == 'member.update':
        print(before.activity, after.activity)
