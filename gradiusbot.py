#! venv3/bin/python

from plugin_loader import PluginLoader
import discord
import asyncio
import configparser
import traceback
import json
import sys
import logging
import time

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
                    asyncio.async(plugin.action(message, client))
                except:
                    print("There was an error with: " + str(plugin))
                    print(traceback.format_exc())

    else:
        if (message.server.id == server_id) or (server_id == ""):
            if not message.author.name == selfname and message.channel.name in permitted_channels:
                for plugin in plugins.public_plugins:
                    try:
                        asyncio.async(plugin.action(message, client))
                    except:
                        print("There was an error with: " + str(plugin))
                        print(traceback.format_exc())


def main_task(config_file):

    loop = asyncio.get_event_loop()

    config.read(config_file)
    email = config.get("Account", "email")
    password = config.get("Account", "password")

    if config.getboolean("BotSettings", "debug"):
        logging.basicConfig(level=logging.DEBUG)

    plugins.load_plugins(config)

    while True:
        try:
            print("Logging in...")
            loop.run_until_complete(client.login(email, password))
            # time.sleep(5)
            client.wait_until_login()
            print("Connecting...")
            client.wait_until_ready()
            print("Ready!")
            loop.run_until_complete(client.connect())
        except KeyboardInterrupt:
            loop.run_until_complete(client.logout())
            print("logging out.")
            time.sleep(3)
        except:
            print(traceback.print_exc())

        print("Logging out...")
        loop.run_until_complete(client.logout())
        print("Closing...")
        print("Ended.")
        time.sleep(2)
if __name__ == "__main__":
        main_task(sys.argv[1])
