#!/usr/bin/env python
# Discord 1.0 docs: http://discordpy.readthedocs.io/en/rewrite/index.html
import discord
import configparser
import traceback
import logging
from sys import argv
from libs import plugin_loader
from asyncio import ensure_future

# Setup Config
config = configparser.RawConfigParser()
try:
    config.read(argv[1])
except:
    print(traceback.format_exc())

# Setup Logging
# TODO: Setup levels via config
logger = logging.getLogger('gradiusbot')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('gradiusbot.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

# Grab config values
token = config.get('gradiusbot', 'token')

# Create the plugin loader
plugins = plugin_loader.PluginLoader()

# Create Discord Client
client = discord.Client()


# When the client is connected and ready
@client.event
async def on_ready():
    logger.info('Logged in as {0.user}'.format(client))


# When the client resumes a session
@client.event
async def on_resumed():
    logger.info('Resumed session as {0.user}'.format(client))


# When the client receives a message
@client.event
async def on_message(message):
    # This message is the bot sending messages
    if message.author == client.user:
        return

    # Is it a private message?
    if isinstance(message.channel, discord.abc.PrivateChannel):
        for plugin in plugins.private_plugins:
            try:
                # Launch the plugin and the method .action
                ensure_future(plugin.action(message, config))
            except:
                logger.error(traceback.format_exc())

    # Is it a Guild Message?
    if isinstance(message.channel, discord.abc.GuildChannel):
        for plugin in plugins.public_plugins:
            try:
                # Launch the plugin and the method .action
                ensure_future(plugin.action(message, config))
            except:
                logger.error(traceback.format_exc())


# When a message is deleted
@client.event
async def on_message_delete(message):
    for plugin in plugins.event_plugins.messages:
        try:
            # Launch the plugin and the method .action
            ensure_future(plugin.action('delete', message, config))
        except:
            logger.error(traceback.format_exc())


# When a message is edited
@client.event
async def on_message_edit(before, after):
    for plugin in plugins.event_plugins.messages:
        try:
            # Launch the plugin and the method .action
            ensure_future(plugin.action('edit', before, config, after=after))
        except:
            logger.error(traceback.format_exc())


# When a reaction is added
@client.event
async def on_reaction_add(reaction, user):
    for plugin in plugins.event_plugins.reactions:
        try:
            # Launch the plugin and the method .action
            ensure_future(plugin.action('add', reaction, config, user=user))
        except:
            logger.error(traceback.format_exc())


# When a reaction is removed
@client.event
async def on_reaction_remove(reaction, user):
    for plugin in plugins.event_plugins.reactions:
        try:
            # Launch the plugin and the method .action
            ensure_future(plugin.action('remove', reaction, config, user=user))
        except:
            logger.error(traceback.format_exc())


# When a message has all reactions removed
@client.event
async def on_reaction_clear(payload):
    for plugin in plugins.event_plugins.reactions:
        try:
            # Launch the plugin and the method .action
            ensure_future(plugin.action('clear', payload, config))
        except:
            logger.error(traceback.format_exc())


# When a private channel is created
@client.event
async def on_private_channel_create(channel):
    pass


@client.event
async def on_private_channel_delete(channel):
    pass


# When a private channel is updated
@client.event
async def on_private_channel_update(before, after):
    pass


# When a message is pinned/unpinned from a private channel
@client.event
async def on_private_channel_pins_update(channel, last_pin):
    pass


# When a guild channel is deleted or created
@client.event
async def on_guild_channel_create(channel):
    pass


@client.event
async def on_guild_channel_delete(channel):
    pass


# When a guild channel is updated
@client.event
async def on_guild_channel_update(before, after):
    pass


# When a guild channel's message is pinned or unpinned
@client.event
async def on_guild_channel_pins_update(channel, last_pin):
    pass


# When a member leaves or joins a guild
@client.event
async def on_member_join(member):
    pass


@client.event
async def on_member_remove(member):
    pass


# When a member updates their profile
@client.event
async def on_member_update(before, after):
    pass


# When the client joins a guild or creates a guild
@client.event
async def on_guild_join(guild):
    pass


# When a guild is removed from the client
@client.event
async def on_guild_remove(guild):
    pass


# When a guild updates
@client.event
async def on_guild_update(before, after):
    pass


# When a guild creates or deletes a role
@client.event
async def on_guild_role_create(role):
    pass


@client.event
async def on_guild_role_delete(role):
    pass


# When a guild updates a role
@client.event
async def on_guild_role_update(before, after):
    pass


# When a guild adds or removes an emoji
@client.event
async def on_guild_emojis_update(guild, before, after):
    pass


# When a guild becomes available or unavailable
@client.event
async def on_guild_available(guild):
    pass


@client.event
async def on_guild_unavailable(guild):
    pass


# When a member updates their voice state
@client.event
async def on_voice_state_update(member, before, after):
    pass


# When a member is banned from a guild
@client.event
async def on_member_ban(guild, user):
    pass


# When a member is unbanned from a guild
@client.event
async def on_member_unban(guild, user):
    pass


# When someone joins/leaves a group (private channel)
@client.event
async def on_group_join(channel, user):
    pass


@client.event
async def on_group_remove(channel, user):
    pass


# When a relationship is added or removed
@client.event
async def on_relationship_add(relationship):
    pass


@client.event
async def on_relationship_remove(relationship):
    pass


# When a relationship is updated (block a friend, friendship is accepted)
@client.event
async def on_relationship_update(before, after):
    pass


if __name__ == '__main__':
    # Load the plugins that are configured in the config file
    logger.debug("Loading plugins...")
    plugins.load_plugins(config)

    # Start the client
    client.run(token)
