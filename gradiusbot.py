#! venv3/bin/python

import discord
import asyncio
import configparser
import traceback
import json
import sys
import logging
import random
from plugin_loader import PluginLoader
from libs.elastic_logging import ElasticLogging


config = configparser.RawConfigParser()
plugins = PluginLoader()
client = discord.Client()
elogging = ElasticLogging()


@client.async_event
def background_tasks():
    for task in plugins.scheduled_tasks:
        try:
            asyncio.ensure_future(task.action(client, config))
        except:
            print("There was an error with: " + str(task))
            print(traceback.format_exc())


@client.async_event
def pick_random_status():
    while not client.is_closed:
        status_set = json.loads(config.get("BotSettings", "statuses"))
        status = random.choice(status_set)
        game = discord.Game(name=status)
        asyncio.ensure_future(client.change_presence(game))
        yield from asyncio.sleep(15)


# When the client has successfully connected to Discord.
@client.async_event
def on_ready():
    print('Logged in as: ', client.user.name, 'with ID:', client.user.id)

    # TODO: re-implement with the right function call
    # asyncio.ensure_future(pick_random_status())


# When the client receives a message
@client.async_event
def on_message(message):
    selfname = config.get("BotSettings", "self_name")
    elastic_logging = config.getboolean("BotSettings", "elastic_logging")
    server_id = config.get("BotSettings", "server_id")

    if message.channel.is_private:
        if not message.author.name == selfname:
            if message.content.lower() == "!help" or message.content.lower() == "help":
                for plugin in plugins.private_plugins:
                    try:
                        yield from client.send_message(message.author, plugin.help_message)
                    except AttributeError:
                        pass
                    except:
                        print(traceback.format_exc())
                        if elastic_logging:
                            elogging.log_message(message, traceback.format_exc(), "private on_message", "except")
                for plugin in plugins.public_plugins:
                    try:
                        yield from client.send_message(message.author, plugin.help_message)
                    except AttributeError:
                        pass
                    except:
                        print(traceback.format_exc())
                        if elastic_logging:
                            elogging.log_message(message, traceback.format_exc(), "private on_message", "except")

            # TODO: Make this an else to avoid looping over !help again
            for plugin in plugins.private_plugins:
                try:
                    asyncio.ensure_future(plugin.action(message, client, config))
                except:
                    print("There was an error with: " + str(plugin))
                    print(traceback.format_exc())
                    if elastic_logging:
                        elogging.log_message(message, traceback.format_exc(), "private on_message", "except")

    else:
        if (message.server.id == server_id) or (server_id == ""):
            if not message.author.name == selfname:
                for plugin in plugins.public_plugins:
                    try:
                        asyncio.ensure_future(plugin.action(message, client, config))
                    except:
                        print("There was an error with: " + str(plugin))
                        print(traceback.format_exc())
                        if elastic_logging:
                            elogging.log_message(message, traceback.format_exc(), "public on_message", "except")


# This event is fired when a message was deleted from a server
@client.async_event
def on_message_delete(message):
    selfname = config.get("BotSettings", "self_name")
    elastic_logging = config.getboolean("BotSettings", "elastic_logging")
    server_id = config.get("BotSettings", "server_id")

    if message.channel.is_private:
        if not message.author.name == selfname:
            # TODO: Implement for private messages
            pass
    else:
        if (message.server.id == server_id) or (server_id == ""):
            if not message.author.name == selfname:
                for plugin in plugins.event_plugins:
                    try:
                        asyncio.ensure_future(plugin.action(message, client, config, "delete"))
                    except:
                        print("There was an error with: " + str(plugin))
                        print(traceback.format_exc())
                        if elastic_logging:
                            elogging.log_message(message, traceback.format_exc(), "public on_message_delete", "except")


# This event is fired when a message has been edited.
@client.async_event
def on_message_edit(message, message_after):
    selfname = config.get("BotSettings", "self_name")
    elastic_logging = config.getboolean("BotSettings", "elastic_logging")
    server_id = config.get("BotSettings", "server_id")

    if message.channel.is_private:
        if not message.author.name == selfname:
            # TODO: Implement for private messages
            pass
    else:
        if (message.server.id == server_id) or (server_id == ""):
            if not message.author.name == selfname:
                for plugin in plugins.event_plugins:
                    try:
                        asyncio.ensure_future(plugin.action(message, client, config, "edit", object_after=message_after))
                    except:
                        print("There was an error with: " + str(plugin))
                        print(traceback.format_exc())
                        if elastic_logging:
                            elogging.log_message(message, traceback.format_exc(), "public on_message_edit", "except")


# This event is fired when a member changes their name/UUID
@client.async_event
def on_member_update(member_before, member_after):
    server_id = config.get("BotSettings", "server_id")
    elastic_logging = config.getboolean("BotSettings", "elastic_logging")
    if (member_after.server.id == server_id) or (server_id == ""):
        for plugin in plugins.event_plugins:
            try:
                asyncio.ensure_future(plugin.action(member_before, client, config, "member_update", object_after=member_after))
            except:
                print("There was an error with: " + str(plugin))
                print(traceback.format_exc())


# This event is fired when a member joins the server
@client.async_event
def on_member_join(member):
    server_id = config.get("BotSettings", "server_id")
    if (member.server.id == server_id) or (server_id == ""):
        for plugin in plugins.event_plugins:
            try:
                asyncio.ensure_future(plugin.action(member, client, config, "member_join"))
            except:
                print("There was an error with: " + str(plugin))
                print(traceback.format_exc())


# Fired when a member leaves the server
@client.async_event
def on_member_remove(member):
    server_id = config.get("BotSettings", "server_id")
    if (member.server.id == server_id) or (server_id == ""):
        for plugin in plugins.event_plugins:
            try:
                asyncio.ensure_future(plugin.action(member, client, config, "member_remove"))
            except:
                print("There was an error with: " + str(plugin))
                print(traceback.format_exc())


# Main processing loop
def main_task(config_file):
    config.read(config_file)
    is_user_account = config.getboolean("Account", "is_user_account")

    if config.getboolean("BotSettings", "debug"):
        logging.basicConfig(level=logging.DEBUG)

    if config.getboolean("BotSettings", "logfile"):
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)
    elastic_logging = config.getboolean("BotSettings", "elastic_logging")

    plugins.load_plugins(config)

    try:
        print("Running client...")
        if is_user_account:
            username = config.get("Account", "username")
            password = config.get("Account", "password")
            client.run(username, password)
        else:
            token = config.get("Account", "token")
            client.loop.create_task(background_tasks())
            client.run(token)
    except KeyboardInterrupt:
        print("Killed by keboard!")
    except:
        print("There was an exception:")
        print(traceback.print_exc())


if __name__ == "__main__":
        main_task(sys.argv[1])
