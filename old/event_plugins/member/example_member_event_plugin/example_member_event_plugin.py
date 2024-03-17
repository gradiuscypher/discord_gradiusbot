import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Member Event Plugin] <example_member_event_plugin.py>: This plugin shows you how to use member events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']

    if event_type == 'member.join':
        member = kwargs['member']
        print("{} member has joined {}".format(member.name, member.guild.name))

    if event_type == 'member.remove':
        member = kwargs['member']
        print("{} member has been removed from {}".format(member.name, member.guild.name))

    if event_type == 'member.update':
        before = kwargs['before']
        after = kwargs['after']
        print("Member has been updated:\n\nbefore:{}\n\nafter:{}".format(before, after))

    if event_type == 'member.voice.update':
        member = kwargs['member']
        before = kwargs['before']
        after = kwargs['after']
        print("Member has updated voice status:\n\nmember:{}\n\nbefore:{}\n\nafter:{}".format(member, before, after))

    if event_type == 'member.ban':
        user = kwargs['user']
        guild = kwargs['guild']
        print("Member {} was banned from guild {}".format(user.name, guild.name))

    if event_type == 'member.unban':
        user = kwargs['user']
        guild = kwargs['guild']
        print("Member {} was unbanned from guild {}".format(user.name, guild.name))
