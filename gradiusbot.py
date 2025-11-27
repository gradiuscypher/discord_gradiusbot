#!/usr/bin/env -S uv run

import contextlib
import json
import os

import discord
from discord.channel import DMChannel, TextChannel
from dotenv import load_dotenv

from libs.router import MessageRouter, MessageType

# import various routes to use their decorators
from libs.routes import examples, memes  # noqa: F401
from libs.task_router import TaskRouter

load_dotenv()  # load all the variables from the env file
bot = discord.Client(intents=discord.Intents.all())

# import task modules to register their tasks
with contextlib.suppress(ImportError):
    from libs.routes import message_cleanup, tasks  # noqa: F401

# load enabled modules
module_env = os.getenv("LOADED_MODULES")
loaded_modules = ["core"]

if module_env:
    loaded_modules = json.loads(module_env)


@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is ready and online!")
    # Start scheduled tasks for enabled modules
    TaskRouter.start_tasks(loaded_modules)


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author != bot.user:
        if isinstance(message.channel, TextChannel):
            await MessageRouter.route(loaded_modules, MessageType.message, message)

        elif isinstance(message.channel, DMChannel):
            await MessageRouter.route(loaded_modules, MessageType.dm, message)


if __name__ == "__main__":
    test = {"bob": 1}
    token = os.getenv("TOKEN")

    if token:
        bot.run(token)  # run the bot with the token
    else:
        raise ValueError("TOKEN is not set")
