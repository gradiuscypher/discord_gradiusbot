#!.venv/bin/python3 gradiusbot.py

import json
import os

import discord
from discord.channel import DMChannel, TextChannel
from dotenv import load_dotenv

from libs.router import MessageRouter, MessageType

# import various routes to use their decorators
from libs.routes import examples, memes  # noqa

load_dotenv()  # load all the variables from the env file
bot = discord.Bot(intents=discord.Intents.all())

# load enabled modules
loaded_modules = os.getenv("LOADED_MODULES")
if loaded_modules:
    loaded_modules = json.loads(loaded_modules)
else:
    loaded_modules = ["core"]


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.event
async def on_message(message: discord.Message):
    print(loaded_modules)
    if message.author != bot.user:
        if isinstance(message.channel, TextChannel):
            await MessageRouter.route(loaded_modules, MessageType.message, message)

        elif isinstance(message.channel, DMChannel):
            await MessageRouter.route(loaded_modules, MessageType.dm, message)


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))  # run the bot with the token
