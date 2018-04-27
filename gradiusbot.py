#!/usr/bin/env python
# Discord 1.0 docs: http://discordpy.readthedocs.io/en/rewrite/index.html
import discord
import configparser
import traceback
from sys import argv

# Setup Config
config = configparser.RawConfigParser()
try:
    config.read(argv[1])
except:
    print(traceback.format_exc())

# Grab config values
token = config.get('gradiusbot', 'token')

# Create Discord Client
client = discord.Client()


@client.event
async def on_ready():
    # TODO: Add logging to this rather than just print
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('hello!')

client.run(token)
