#! venv3/bin/python

from plugin_loader import PluginLoader
import discord
import asyncio
import configparser
import traceback
import json
import sys
import logging
import twitter


config = configparser.RawConfigParser()
plugins = PluginLoader()
client = discord.Client()


@client.async_event
def on_ready():
    print('Logged in as: ', client.user.name, 'with ID:', client.user.id)


@client.async_event
def on_message(message):
    selfname = config.get("BotSettings", "self_name")
    permitted_channels = json.loads(config.get('BotSettings', 'permitted_channels'))
    server_id = config.get("BotSettings", "server_id")

    if message.channel.is_private:
        if not message.author.name == selfname:
            for plugin in plugins.private_plugins:
                try:
                    asyncio.async(plugin.action(message, client, config))
                except:
                    print("There was an error with: " + str(plugin))
                    print(traceback.format_exc())

    else:
        if (message.server.id == server_id) or (server_id == ""):
            if not message.author.name == selfname and message.channel.name in permitted_channels:
                for plugin in plugins.public_plugins:
                    try:
                        asyncio.async(plugin.action(message, client, config))
                    except:
                        print("There was an error with: " + str(plugin))
                        print(traceback.format_exc())


@client.async_event
def on_message_delete(message):
    selfname = config.get("BotSettings", "self_name")
    permitted_channels = json.loads(config.get('BotSettings', 'permitted_channels'))
    server_id = config.get("BotSettings", "server_id")

    if message.channel.is_private:
        if not message.author.name == selfname:
            # TODO: Implement for private messages
            pass
    else:
        if (message.server.id == server_id) or (server_id == ""):
            if not message.author.name == selfname and message.channel.name in permitted_channels:
                for plugin in plugins.event_plugins:
                    try:
                        asyncio.async(plugin.action(message, client, config, "delete"))
                    except:
                        print("There was an error with: " + str(plugin))
                        print(traceback.format_exc())


@client.async_event
def on_message_edit(message, message_after):
    selfname = config.get("BotSettings", "self_name")
    permitted_channels = json.loads(config.get('BotSettings', 'permitted_channels'))
    server_id = config.get("BotSettings", "server_id")

    if message.channel.is_private:
        if not message.author.name == selfname:
            # TODO: Implement for private messages
            pass
    else:
        if (message.server.id == server_id) or (server_id == ""):
            if not message.author.name == selfname and message.channel.name in permitted_channels:
                for plugin in plugins.event_plugins:
                    try:
                        asyncio.async(plugin.action(message, client, config, "edit", object_after=message_after))
                    except:
                        print("There was an error with: " + str(plugin))
                        print(traceback.format_exc())


@client.async_event
def on_member_update(member_before, member_after):
    server_id = config.get("BotSettings", "server_id")
    if (member_after.server.id == server_id) or (server_id == ""):
        for plugin in plugins.event_plugins:
            try:
                asyncio.async(plugin.action(member_before, client, config, "member_update", object_after=member_after))
            except:
                print("There was an error with: " + str(plugin))
                print(traceback.format_exc())


def main_task(config_file):
    config.read(config_file)
    email = config.get("Account", "email")
    password = config.get("Account", "password")

    if config.getboolean("BotSettings", "debug"):
        logging.basicConfig(level=logging.DEBUG)

    plugins.load_plugins(config)

    try:
        print("Running client...")
        client.run(email, password)
    except KeyboardInterrupt:
        print("Killed by keboard!")
    except:
        print("There was an exception:")
        print(traceback.print_exc())

        if config.getboolean("BotSettings", "twitter_alert"):
            access_key = config.get("Twitter", "access_key")
            access_secret = config.get("Twitter", "access_secret")
            consumer_key = config.get("Twitter", "consumer_key")
            consumer_secret = config.get("Twitter", "consumer_secret")
            tapi = twitter.Twitter(auth=twitter.OAuth(access_key, access_secret, consumer_key, consumer_secret))

            tapi.statuses.update(status="@RiotGradius, I'm no longer in Discord.")


if __name__ == "__main__":
        main_task(sys.argv[1])
