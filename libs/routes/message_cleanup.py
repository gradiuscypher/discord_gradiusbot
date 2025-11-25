import json
import logging
import os
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import discord
from discord import TextChannel, Thread
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()  # load all the variables from the env file

saved_messages_str = os.getenv("LOADED_MODULES")

if saved_messages_str:
    saved_messages: set[int] = json.loads(saved_messages_str)
else:
    saved_messages = set()

if TYPE_CHECKING:
    from discord.ext.commands import Bot

logger = logging.getLogger(__name__)

CHANNEL_ID = int(os.getenv("TARGET_CLEAN_CHANNEL"))
MESSAGE_ALLOWLIST = saved_messages


class MessageCleanupTask:
    def __init__(
        self,
        bot: "Bot",
        channel_id: int,
        hours: int = 72,
        allowlist: set[int] | None = None,
    ) -> None:
        self.bot = bot
        self.channel_id = channel_id
        self.hours = hours
        self.allowlist = allowlist or set()

    @tasks.loop(hours=1)
    async def cleanup_old_messages(self) -> None:
        """Delete messages older than specified hours from the channel."""
        try:
            channel = self.bot.get_channel(self.channel_id)
            if not channel:
                logger.error("Channel %s not found", self.channel_id)
                return

            # Ensure the channel supports message history
            if not isinstance(channel, (TextChannel, Thread)):
                logger.error(
                    "Channel %s is not a text-based channel",
                    self.channel_id,
                )
                return

            cutoff_time = datetime.now(UTC) - timedelta(hours=self.hours)
            deleted_count = 0

            # Fetch messages older than cutoff time
            async for message in channel.history(
                limit=None,
                before=cutoff_time,
                oldest_first=False,
            ):
                # Skip allowlisted messages
                if message.id in self.allowlist:
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
                self.channel_id,
            )

        except Exception:
            logger.exception("Error in cleanup_old_messages task: %s")

    @cleanup_old_messages.before_loop
    async def before_cleanup(self) -> None:
        """Wait until the bot is ready before starting the task."""
        await self.bot.wait_until_ready()

    def start(self) -> None:
        """Start the cleanup task."""
        self.cleanup_old_messages.start()

    def stop(self) -> None:
        """Stop the cleanup task."""
        self.cleanup_old_messages.cancel()

    def add_to_allowlist(self, message_id: int) -> None:
        """Add a message ID to the allowlist."""
        self.allowlist.add(message_id)

    def remove_from_allowlist(self, message_id: int) -> None:
        """Remove a message ID from the allowlist."""
        self.allowlist.discard(message_id)


# Usage example
def setup_cleanup_task(bot: "Bot") -> MessageCleanupTask:
    """Initialize and start the cleanup task."""
    cleanup = MessageCleanupTask(
        bot=bot,
        channel_id=CHANNEL_ID,
        hours=72,
        allowlist=MESSAGE_ALLOWLIST,
    )
    cleanup.start()
    return cleanup
