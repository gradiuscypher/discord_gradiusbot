import asyncio
import logging
from discord import utils
from discord import Embed, Color

logger = logging.getLogger('gradiusbot')

logger.info("[Member Event Plugin] <spotify_tracking.py>: This plugin monitors Spotify events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']

    if event_type == 'member.update':
        after = kwargs['after']

        if after.activity:
            if after.activity.type.name == 'listening':
                target_channel = utils.get(after.guild.channels, name='general')
                spotify_obj = after.activity
                spotify_embed = Embed(title='Spotify Tracker', color=spotify_obj.color)
                spotify_embed.set_thumbnail(url=spotify_obj.album_cover_url)
                spotify_embed.set_author(name=after.name, icon_url=after.avatar_url)
                spotify_embed.add_field(name='Song', value=spotify_obj.title, inline=True)
                spotify_embed.add_field(name='Artist', value=spotify_obj.artist, inline=True)
                spotify_embed.add_field(name='Album', value=spotify_obj.album, inline=True)
                spotify_embed.set_footer(text=spotify_obj.track_id)
                await target_channel.send(embed=spotify_embed)
