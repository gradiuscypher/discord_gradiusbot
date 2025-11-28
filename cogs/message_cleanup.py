import json
import logging
import os
from datetime import UTC, datetime, timedelta

import discord
from discord import TextChannel, Thread
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the env file

saved_messages_str = os.getenv("SAVED_MESSAGES")

if saved_messages_str:
    saved_messages: list[int] = json.loads(saved_messages_str)
else:
    saved_messages: list[int] = []

logger = logging.getLogger(__name__)


CHANNEL_ID = int(os.getenv("TARGET_CLEAN_CHANNEL"))
MESSAGE_ALLOWLIST = saved_messages
CLEANUP_HOURS = 72
CLEANUP_SECONDS = 5
UPDATE_MESSAGE_COUNT = 10

print(MESSAGE_ALLOWLIST)


class MessageCleanup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.cleanup.start()

    @tasks.loop(minutes=1)
    async def cleanup(self) -> None:
        logger.info("Starting message cleanup...")
        channel = self.bot.get_channel(CHANNEL_ID)
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
        processed_count = 0

        # Fetch messages older than cutoff time
        async for message in channel.history(
            limit=None,
            before=cutoff_time,
            oldest_first=False,
        ):
            processed_count += 1

            # Report status every 50 messages
            if processed_count % UPDATE_MESSAGE_COUNT == 0:
                logger.info(
                    "Progress: Processed %s messages, deleted %s",
                    processed_count,
                    deleted_count,
                )

            # Skip allowlisted messages
            if message.id in MESSAGE_ALLOWLIST:
                logger.info("Message ID %s is in allowlist.", message.id)
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
            "Cleanup complete: Processed %s messages, deleted %s from channel %s",
            processed_count,
            deleted_count,
            CHANNEL_ID,
        )


async def setup(bot: commands.Bot) -> None:
    logger.info("Loading MessageCleanup Cog")
    await bot.add_cog(MessageCleanup(bot))
