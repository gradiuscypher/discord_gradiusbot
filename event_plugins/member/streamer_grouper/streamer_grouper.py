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
        guild = member_after.guild
        debug_channel = utils.get(guild.channels, name='debug')
        streaming_role = utils.get(guild.roles, name='streaming')

        # Debug
        print("Member Update!\nbefore:{}\nafter:{}".format(before_activity, after_activity))

        # If the user is going from no activity to streaming
        if before_activity is None:
            if after_activity and after_activity.type.name == 'listening' and streaming_after is None:
                print('User is streaming and is not in the streaming group')
                await member_after.add_roles(streaming_role, reason='{} started streaming.'.format(member_after.name))
                await debug_channel.send('{} is streaming!'.format(member_after.name))
                return

        # If the user is going from another activity to streaming and isn't in the streamer group
        if before_activity and not streaming_before:
            if after_activity and after_activity.type.name == 'listening' and streaming_after is None:
                print("User is streaming, and was doing something else before, and is not in the streamers group")
                await member_after.add_roles(streaming_role, reason='{} started streaming.'.format(member_after.name))
                await debug_channel.send('{} is streaming!'.format(member_after.name))
                return

        # If the user was streaming before
        if streaming_before:
            # If the user is doing something else that's not streaming
            if after_activity and after_activity.type.name != 'listening':
                print("The User was streaming before and now is no longer streaming but is doing something else")
                await member_after.remove_roles(streaming_role, reason='{} stopped streaming.'.format(member_after.name))
                await debug_channel.send('{} is NOT streaming!'.format(member_after.name))
                return
            # If the user isn't doing anything else
            if not after_activity:
                print("The User was streaming before and now is no longer streaming or doing anything")
                await member_after.remove_roles(streaming_role, reason='{} stopped streaming.'.format(member_after.name))
                await debug_channel.send('{} is NOT streaming!'.format(member_after.name))
                return
