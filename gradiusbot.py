#!/usr/bin/env -S uv run

import json
import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

NOT_SET_WARNING = "Discord token environment variable is not set."

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to see all messages
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


load_dotenv()  # load all the variables from the env file
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


async def load_cogs() -> None:
    # Get the list of cogs to load from the .env file
    loaded_modules = os.getenv("LOADED_MODULES")

    if loaded_modules:
        try:
            # Parse the JSON array from the environment variable
            cog_list = json.loads(loaded_modules)

            # Load each specified cog
            for cog_name in cog_list:
                try:
                    await bot.load_extension(f"cogs.{cog_name}")
                    print(f"✓ Loaded cog: {cog_name}")
                except Exception as e:
                    print(f"✗ Failed to load cog '{cog_name}': {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing LOADED_MODULES: {e}")
            print("Loading all cogs from directory as fallback...")
            await load_all_cogs()
    else:
        print("LOADED_MODULES not set, loading all cogs from directory...")
        await load_all_cogs()


async def load_all_cogs() -> None:
    """Fallback function to load all cogs from the cogs directory"""
    cogs_dir = Path("./cogs")
    for cog_file in cogs_dir.glob("*.py"):
        if not cog_file.name.startswith("_"):
            await bot.load_extension(f"cogs.{cog_file.stem}")


@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is ready and online!")
    print("Loading cogs directory...")
    await load_cogs()

    # Only sync in development
    if os.getenv("ENV") == "development":
        print("Syncing command tree...")
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")


@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context) -> None:
    """Manually sync slash commands globally"""
    synced = await bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} command(s)")


@bot.command()
@commands.is_owner()
async def syncguild(ctx: commands.Context) -> None:
    """Sync slash commands to current guild only (faster for testing)"""
    bot.tree.copy_global_to(guild=ctx.guild)
    synced = await bot.tree.sync(guild=ctx.guild)
    await ctx.send(f"Synced {len(synced)} command(s) to this guild")


if __name__ == "__main__":
    token = os.getenv("TOKEN")

    if token:
        bot.run(token)  # run the bot with the token
    else:
        raise ValueError(NOT_SET_WARNING)
