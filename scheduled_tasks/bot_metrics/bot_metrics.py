import asyncio
import logging
import traceback
from concurrent.futures import CancelledError

# Setup Logging
logger = logging.getLogger('gradiusbot')
logger.setLevel(logging.DEBUG)

logger.info("[Scheduled Task] <bot_metrics.py>: Collects metrics about the bot every hour.")


async def action(client, config):
    while True:
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
                await asyncio.sleep(3600)
            else:
                await asyncio.sleep(10)

        # ref: https://stackoverflow.com/questions/38652819/from-concurrent-futures-to-asyncio
        except CancelledError:
            raise NotImplementedError

        except RuntimeError:
            logger.error(traceback.format_exc())
            exit(0)

        except:
            logger.error(traceback.format_exc())
