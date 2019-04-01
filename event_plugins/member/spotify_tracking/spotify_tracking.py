import asyncio
import logging
import traceback
from datetime import datetime, timedelta
from discord import utils

logger = logging.getLogger('gradiusbot')
spotify_logger = logging.getLogger('spotify_tracking')

logger.info("[Member Event Plugin] <spotify_tracking.py>: This plugin monitors Spotify events.")

# track_cache[member.id] = {'track_id': spotify.track_id}
track_cache = {}


def log_event(elastic, title, artists, album, track_id, duration, party_id, member_id, member_name, guild_id):
    index_name = f"spotify-events-{datetime.now().strftime('%Y-%m')}"
    log_body = {
        'guild_id': guild_id,
        'member_id': member_id,
        'member_name': member_name,
        'title': title,
        'artists': artists,
        'album': album,
        'track_id': track_id,
        'duration': duration,
        'party_id': party_id,
        'timestamp': datetime.utcnow()
    }
    elastic.index(index=index_name, doc_type='spotify-event', body=log_body)


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']
    elastic = kwargs['elastic']

    if event_type == 'member.update':
        after = kwargs['after']
        before = kwargs['before']
        monitoring_role = utils.get(after.roles, name='monitoring')

        if monitoring_role and after.activity:
            if after.activity.type.name == 'listening':
                spotify_obj = after.activity
                spotify_before = before.activity

                try:
                    if spotify_before and spotify_obj:
                        if spotify_before.end <= (spotify_obj.start + timedelta(seconds=5)):
                            if not (after.id in track_cache.keys() and spotify_obj.track_id == track_cache[after.id]['track_id']):
                                spotify_logger.debug(f"new song not cached, {spotify_before.title}, "
                                                     f"{spotify_before.artists}, {spotify_before.album}, "
                                                     f"{spotify_before.track_id}, {spotify_before.duration.seconds}, "
                                                     f"{spotify_before.party_id}")
                                track_cache[after.id] = {'track_id': spotify_obj.track_id}
                                log_event(elastic, spotify_before.title, spotify_before.artists, spotify_before.album,
                                          spotify_before.track_id, spotify_before.duration.seconds,
                                          spotify_before.party_id, before.id, before.name, before.guild.id)

                    elif spotify_before and spotify_obj is None:
                        if spotify_before.end <= (datetime.utcnow() + timedelta(seconds=5)):
                            if not (after.id in track_cache.keys() and spotify_obj.track_id == track_cache[after.id]['track_id']):
                                spotify_logger.debug(f"last song not cached, {spotify_before.title}, "
                                                     f"{spotify_before.artists}, {spotify_before.album}, "
                                                     f"{spotify_before.track_id}, {spotify_before.duration.seconds}, "
                                                     f"{spotify_before.party_id}")
                                track_cache[after.id] = {'track_id': spotify_obj.track_id}
                                log_event(elastic, spotify_before.title, spotify_before.artists, spotify_before.album,
                                          spotify_before.track_id, spotify_before.duration.seconds,
                                          spotify_before.party_id, before.id, before.name, before.guild.id)
                except:
                    spotify_logger.error(traceback.format_exc())
                    logger.error(traceback.format_exc())
