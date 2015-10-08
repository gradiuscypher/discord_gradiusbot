#!venv/bin/python

import discord
import configparser
import json
import traceback
from threading import Thread
from plugin_loader import PluginLoader


config = configparser.RawConfigParser()
config.read('config.conf')

username = config.get('Discord', 'username')
password = config.get('Discord', 'password')
selfname = config.get('Discord', 'selfname')
permitted_channels = json.loads(config.get('Discord', 'permitted_channels'))

client = discord.Client()
client.login(username, password)

p_loader = PluginLoader()
p_loader.load_plugins()


@client.event
def on_ready():
    print("Connected")

    for s in client.servers:
        chan_names = []
        for c in s.channels:
            chan_names.append(c.name)
        print(s.name + str(chan_names))


@client.event
def on_message(message):

    if message.channel.is_private:
        if not message.author.name == selfname:
            for plugin in p_loader.private_plugins:
                try:
                    t = Thread(target=plugin.action, args=(message, client.send_message))
                    t.start()
                except:
                    print("There was an error with: " + str(plugin))
                    print(traceback.format_exc())

    else:
        if not message.author.name == selfname and message.channel.name in permitted_channels:
            for plugin in p_loader.public_plugins:
                try:
                    t = Thread(target=plugin.action, args=(message, client.send_message))
                    t.start()
                except:
                    print("There was an error with: " + str(plugin))
                    print(traceback.format_exc())

client.run()
