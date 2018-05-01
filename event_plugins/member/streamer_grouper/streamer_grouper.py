import asyncio
import logging
from discord import utils

logger = logging.getLogger('gradiusbot')

logger.info("[Member Event Plugin] <streamer_grouper.py>: This plugin groups people who are streaming.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']

    if event_type == 'member.update':
        member_before = kwargs['before']
        member_after = kwargs['after']
        before_activity = member_before.activity
        after_activity = member_after.activity
        streaming_before = utils.get(member_before.roles, name='streaming')
        streaming_after = utils.get(member_after.roles, name='streaming')

        if after_activity and after_activity.type.name == 'listening' and streaming_after is None:
            # the user is streaming
            guild = member_after.guild
            debug_channel = utils.get(guild.channels, name='debug')
            streaming_role = utils.get(guild.roles, name='streaming')
            await member_after.add_roles(streaming_role, reason='{} started streaming.'.format(member_after.name))
            await debug_channel.send('{} is streaming!'.format(member_after.name))

        if streaming_before and before_activity and before_activity.type.name == 'listening' and after_activity != 'listening':
            # the user is not streaming
            guild = member_after.guild
            debug_channel = utils.get(guild.channels, name='debug')
            streaming_role = utils.get(guild.roles, name='streaming')
            await member_after.remove_roles(streaming_role, reason='{} stopped streaming.'.format(member_after.name))
            await debug_channel.send('{} is NOT streaming!'.format(member_after.name))
