import json
import logging
import os
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import discord
from discord import TextChannel, Thread
from discord.ext import tasks
from dotenv import load_dotenv

from libs.task_router import TaskRouter

if TYPE_CHECKING:
    from discord.ext.commands import Bot

load_dotenv()  # load all the variables from the env file

saved_messages_str = os.getenv("LOADED_MODULES")

if saved_messages_str:
    saved_messages: set[int] = json.loads(saved_messages_str)
else:
    saved_messages = set()

logger = logging.getLogger(__name__)

CHANNEL_ID = int(os.getenv("TARGET_CLEAN_CHANNEL"))
MESSAGE_ALLOWLIST = saved_messages
CLEANUP_HOURS = 72

# Module-level bot reference, set during bot initialization
bot: "Bot | None" = None


@TaskRouter("cleanup")
@tasks.loop(seconds=10)
async def cleanup_old_messages() -> None:
    """Delete messages older than specified hours from the channel."""
    print("Starting message_cleanup")
    try:
        if bot is None:
            logger.error("Bot instance not available")
            return

        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            logger.error("Channel %s not found", CHANNEL_ID)
            return

        # Ensure the channel supports message history
        if not isinstance(channel, (TextChannel, Thread)):
            logger.error(
                "Channel %s is not a text-based channel",
                CHANNEL_ID,
            )
            return

        cutoff_time = datetime.now(UTC) - timedelta(hours=CLEANUP_HOURS)
        deleted_count = 0

        # Fetch messages older than cutoff time
        async for message in channel.history(
            limit=None,
            before=cutoff_time,
            oldest_first=False,
        ):
            # Skip allowlisted messages
            if message.id in MESSAGE_ALLOWLIST:
                continue

            # Skip messages newer than cutoff
            if message.created_at > cutoff_time:
                continue

            try:
                await message.delete()
                deleted_count += 1
            except discord.NotFound:
                # Message already deleted
                pass
            except discord.Forbidden:
                logger.exception(
                    "Missing permissions to delete message %s",
                    message.id,
                )
            except discord.HTTPException:
                logger.exception("Failed to delete message %s", message.id)

        logger.info(
            "Deleted %s messages from channel %s",
            deleted_count,
            CHANNEL_ID,
        )

    except Exception:
        logger.exception("Error in cleanup_old_messages task: %s")
