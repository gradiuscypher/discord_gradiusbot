import asyncio
import logging
import traceback
from concurrent.futures import CancelledError
from discord.ext.tasks import loop

# Setup Logging
logger = logging.getLogger('gradiusbot')
logger.setLevel(logging.DEBUG)

logger.info("[Scheduled Task] <bot_metrics.py>: Collects metrics about the bot every hour.")


async def action(client, config):
    @loop(seconds=3600)
    async def collect_metrics():
        try:
            if client.is_ready():
                logger.debug("Starting bot metrics collection...")
                # collect the metrics about guilds
                guild_names = []

                for guild in client.guilds:
                    guild_names.append(guild.name)

                metrics_dict = {
                    'total_guilds': len(client.guilds),
                    'guild_names': guild_names
                }
                logger.info("Metrics collection complete. Waiting 1 hour.", extra=metrics_dict)

        except RuntimeError:
            logger.error(traceback.format_exc())
            exit(0)

        except:
            logger.error(traceback.format_exc())

    @collect_metrics.before_loop
    async def before_loop():
        logger.info("Waiting for client to log in before starting metrics task...")
        await client.wait_until_ready()

    collect_metrics.start()
