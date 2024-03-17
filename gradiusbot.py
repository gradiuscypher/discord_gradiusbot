#!.venv/bin/python3 gradiusbot.py

import os

import discord
from discord.channel import DMChannel, TextChannel
from dotenv import load_dotenv

from libs.router import MessageRouter, MessageType

# import various routes to use their decorators
from libs.routes import message_routes  # noqa

load_dotenv()  # load all the variables from the env file
bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.event
async def on_message(message: discord.Message):
    if isinstance(message.channel, TextChannel):
        await MessageRouter.route(MessageType.message, message)

    elif isinstance(message.channel, DMChannel):
        await MessageRouter.route(MessageType.dm, message)


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))  # run the bot with the token
