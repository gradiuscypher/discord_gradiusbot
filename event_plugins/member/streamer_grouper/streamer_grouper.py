import asyncio
import logging
from discord import utils

logger = logging.getLogger('gradiusbot')

logger.info("[Member Event Plugin] <streamer_grouper.py>: This plugin groups people who are streaming.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']
    config = kwargs['config']
    debug_channel_name = config.get('gradiusbot', 'debug_channel')
    debug = config.getboolean('gradiusbot', 'debug')

    if event_type == 'member.update':
        member_before = kwargs['before']
        member_after = kwargs['after']
        before_activity = member_before.activity
        after_activity = member_after.activity
        streaming_before = utils.get(member_before.roles, name='streaming')
        streaming_after = utils.get(member_after.roles, name='streaming')
        guild = member_after.guild
        debug_channel = utils.get(guild.channels, name=debug_channel_name)
        streaming_role = utils.get(guild.roles, name='streaming')

        # If the user is going from no activity to streaming
        if before_activity is None:
            if after_activity and after_activity.type.name == 'streaming' and streaming_after is None:
                await member_after.add_roles(streaming_role, reason='{} started streaming.'.format(member_after.name))
                if debug:
                    await debug_channel.send('{} is streaming!'.format(member_after.name))
                return

        # If the user is going from another activity to streaming and isn't in the streamer group
        if before_activity and not streaming_before:
            if after_activity and after_activity.type.name == 'streaming' and streaming_after is None:
                await member_after.add_roles(streaming_role, reason='{} started streaming.'.format(member_after.name))
                if debug:
                    await debug_channel.send('{} is streaming!'.format(member_after.name))
                return

        # If the user was streaming before
        if streaming_before:
            # If the user is doing something else that's not streaming
            if after_activity and after_activity.type.name != 'streaming':
                await member_after.remove_roles(streaming_role, reason='{} stopped streaming.'.format(member_after.name))
                if debug:
                    await debug_channel.send('{} is NOT streaming!'.format(member_after.name))
                return
            # If the user isn't doing anything else
            if not after_activity:
                await member_after.remove_roles(streaming_role, reason='{} stopped streaming.'.format(member_after.name))
                if debug:
                    await debug_channel.send('{} is NOT streaming!'.format(member_after.name))
                return
