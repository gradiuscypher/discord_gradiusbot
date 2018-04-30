import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Guild Event Plugin] <example_guild_event_plugin.py>: This plugin shows you how to use guild events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']

    if event_type == 'guild.channel.create':
        channel = kwargs['channel']
        print("A channel named {} was created in the guild named {}".format(channel.name, channel.guild.name))

    if event_type == 'guild.channel.delete':
        channel = kwargs['channel']
        print("A channel named {} was deleted in the guild named {}".format(channel.name, channel.guild.name))

    if event_type == 'guild.channel.update':
        before = kwargs['before']
        after = kwargs['after']
        print("A channel was updated in {}.\n\nbefore:{}\n\nafter:{}".format(before.guild.name, before, after))

    if event_type == 'guild.channel.pins.update':
        channel = kwargs['channel']
        last_pin = kwargs['last_pin']
        print("{} had its pins updated. Last pin datetime was {}".format(channel.name, last_pin))

    if event_type == 'guild.update':
        before = kwargs['before']
        after = kwargs['after']
        print("{} was updated.\n\nbefore:{}\n\nafter:{}".format(before.name, before, after))

    if event_type == 'guild.role.create':
        role = kwargs['role']
        print("{} role was created on {}".format(role.name, role.guild.name))

    if event_type == 'guild.role.delete':
        role = kwargs['role']
        print("{} role was deleted on {}".format(role.name, role.guild.name))

    if event_type == 'guild.role.update':
        before = kwargs['before']
        after = kwargs['after']
        print("{} guild has updated a role.\n\nbefore:{}\n\nafter:{}".format(before.guild.name, before, after))

    if event_type == 'guild.emoji.update':
        guild = kwargs['guild']
        before = kwargs['before']
        after = kwargs['after']
        print("{} guild has had its emojis updated.\n\nbefore:{}\n\nafter:{}".format(guild.name, before, after))
