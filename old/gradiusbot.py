#!/usr/bin/env python
import discord
import elasticsearch
import json
import logging
import traceback
from libs import plugin_loader
from libs.json_logging import CustomJsonFormatter
from asyncio import ensure_future

# Setup Config
try:
    with open('conf/config.json') as json_file:
        config_json = json.loads(json_file.read())
except:
    print(traceback.format_exc())

# Setup Logging
# TODO: Setup levels via config
logger = logging.getLogger('gradiusbot')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('gradiusbot.json')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
json_formatter = CustomJsonFormatter()
fh.setFormatter(json_formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# Grab config values
token = config_json['token']

# Create the plugin loader
plugins = plugin_loader.PluginLoader()

# Setup the elasticsearch object for any plugins that want it
if 'elastic_url' in config_json.keys():
    elastic = elasticsearch.Elasticsearch(config_json['elastic_url'])
else:
    elastic = None

# Create Discord Client
# set the bot's intents
# https://discordpy.readthedocs.io/en/latest/intents.html

intents = discord.Intents.all()
client = discord.Client(intents=intents)


async def background_tasks():
    for task in plugins.scheduled_tasks:
        try:
            await ensure_future(task.action(client, config_json))
        except:
            print("There was an error with: " + str(task))
            print(traceback.format_exc())


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
                await ensure_future(plugin.action(message=message, config=config_json, client=client, elastic=elastic))
            except:
                logger.error(traceback.format_exc())

    # Is it a Guild Message?
    if isinstance(message.channel, discord.abc.GuildChannel):
        for plugin in plugins.public_plugins:
            try:
                # Launch the plugin and the method .action
                await ensure_future(plugin.action(message=message, config=config_json, client=client, elastic=elastic))
            except:
                logger.error(traceback.format_exc())


# When a message is deleted
@client.event
async def on_message_delete(message):
    for plugin in plugins.event_plugins.messages:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='delete', message=message, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a message is edited
@client.event
async def on_message_edit(before, after):
    for plugin in plugins.event_plugins.messages:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='edit', before=before, after=after, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a reaction is added
@client.event
async def on_reaction_add(reaction, user):
    for plugin in plugins.event_plugins.reactions:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='add', reaction=reaction, user=user, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a reaction is added - raw event
@client.event
async def on_raw_reaction_add(payload):
    for plugin in plugins.event_plugins.reactions:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='raw_add', payload=payload, client=client, elastic=elastic, config=config_json))
        except:
            logger.error(traceback.format_exc())


# When a reaction is removed
@client.event
async def on_reaction_remove(reaction, user):
    for plugin in plugins.event_plugins.reactions:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='remove', reaction=reaction, user=user, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a reaction is removed - raw event
@client.event
async def on_raw_reaction_remove(payload):
    for plugin in plugins.event_plugins.reactions:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='raw_remove', payload=payload, client=client, elastic=elastic, config=config_json))
        except:
            logger.error(traceback.format_exc())


# When a message has all reactions removed
@client.event
async def on_reaction_clear(message, reactions):
    for plugin in plugins.event_plugins.reactions:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='clear', message=message, reactions=reactions, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a private channel is created
@client.event
async def on_private_channel_create(channel):
    for plugin in plugins.event_plugins.private_channels:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='create', channel=channel, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


@client.event
async def on_private_channel_delete(channel):
    for plugin in plugins.event_plugins.private_channels:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='delete', channel=channel, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a private channel is updated
@client.event
async def on_private_channel_update(before, after):
    for plugin in plugins.event_plugins.private_channels:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='delete', before=before, after=after, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a message is pinned/unpinned from a private channel
@client.event
async def on_private_channel_pins_update(channel, last_pin):
    for plugin in plugins.event_plugins.private_channels:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='pin.update', channel=channel, last_pin=last_pin, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a guild channel is deleted or created
@client.event
async def on_guild_channel_create(channel):
    for plugin in plugins.event_plugins.guild:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='guild.channel.create', channel=channel, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


@client.event
async def on_guild_channel_delete(channel):
    for plugin in plugins.event_plugins.guild:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='guild.channel.delete', channel=channel, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a guild channel is updated
@client.event
async def on_guild_channel_update(before, after):
    for plugin in plugins.event_plugins.guild:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='guild.channel.update', before=before, after=after, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a guild channel's message is pinned or unpinned, last_pin is None if there are no pins
@client.event
async def on_guild_channel_pins_update(channel, last_pin):
    for plugin in plugins.event_plugins.guild:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='guild.channel.pins.update', channel=channel, last_pin=last_pin, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a member leaves or joins a guild
@client.event
async def on_member_join(member):
    for plugin in plugins.event_plugins.member:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='member.join', member=member, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


@client.event
async def on_member_remove(member):
    for plugin in plugins.event_plugins.member:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='member.remove', member=member, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a member updates their profile
@client.event
async def on_member_update(before, after):
    for plugin in plugins.event_plugins.member:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='member.update', before=before, after=after, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When the client joins a guild or creates a guild
@client.event
async def on_guild_join(guild):
    for plugin in plugins.event_plugins.client:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='client.guild.join', guild=guild, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a guild is removed from the client
@client.event
async def on_guild_remove(guild):
    for plugin in plugins.event_plugins.client:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='client.guild.remove', guild=guild, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a guild updates
@client.event
async def on_guild_update(before, after):
    for plugin in plugins.event_plugins.guild:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='guild.update', before=before, after=after, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a guild creates or deletes a role
@client.event
async def on_guild_role_create(role):
    for plugin in plugins.event_plugins.guild:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='guild.role.create', role=role, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


@client.event
async def on_guild_role_delete(role):
    for plugin in plugins.event_plugins.guild:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='guild.role.delete', role=role, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a guild updates a role
@client.event
async def on_guild_role_update(before, after):
    for plugin in plugins.event_plugins.guild:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='guild.role.update', before=before, after=after, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a guild adds or removes an emoji
@client.event
async def on_guild_emojis_update(guild, before, after):
    for plugin in plugins.event_plugins.guild:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='guild.emoji.update', guild=guild, before=before, after=after, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a guild becomes available or unavailable
@client.event
async def on_guild_available(guild):
    for plugin in plugins.event_plugins.client:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='client.guild.available', guild=guild, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


@client.event
async def on_guild_unavailable(guild):
    for plugin in plugins.event_plugins.client:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='client.guild.unavailable', guild=guild, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a member updates their voice state
@client.event
async def on_voice_state_update(member, before, after):
    for plugin in plugins.event_plugins.member:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='member.voice.update', member=member, before=before, after=after, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a member is banned from a guild
@client.event
async def on_member_ban(guild, user):
    for plugin in plugins.event_plugins.member:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='member.ban', guild=guild, user=user, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a member is unbanned from a guild
@client.event
async def on_member_unban(guild, user):
    for plugin in plugins.event_plugins.member:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='member.unban', guild=guild, user=user, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When someone joins/leaves a group (private channel)
@client.event
async def on_group_join(channel, user):
    for plugin in plugins.event_plugins.group:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='group.join', channel=channel, user=user, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


@client.event
async def on_group_remove(channel, user):
    for plugin in plugins.event_plugins.group:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='group.remove', channel=channel, user=user, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a relationship is added or removed
@client.event
async def on_relationship_add(relationship):
    for plugin in plugins.event_plugins.relationships:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='relationship.add', relationship=relationship, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


@client.event
async def on_relationship_remove(relationship):
    for plugin in plugins.event_plugins.relationships:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='relationship.remove', relationship=relationship, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


# When a relationship is updated (block a friend, friendship is accepted)
@client.event
async def on_relationship_update(before, after):
    for plugin in plugins.event_plugins.relationships:
        try:
            # Launch the plugin and the method .action
            await ensure_future(plugin.action(event_type='relationship.update', before=before, after=after, config=config_json, client=client, elastic=elastic))
        except:
            logger.error(traceback.format_exc())


if __name__ == '__main__':
    try:
        # Load the plugins that are configured in the config file
        logger.debug("Loading plugins...")
        plugins.load_plugins(config_json)

        # Setup scheduled tasks loop
        client.loop.create_task(background_tasks())

        # Start the client
        is_bot_token = config_json['is_bot_token']
        client.run(token, bot=is_bot_token)

    except KeyboardInterrupt:
        print("Killed by keyboard!")
        exit(0)

    except:
        print("There was an exception:")
        print(traceback.print_exc())
