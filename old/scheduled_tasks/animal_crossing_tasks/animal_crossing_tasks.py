import asyncio
import logging
import traceback
from libs.ac_libs import AcManager
from public_plugins.animal_crossing.animal_crossing import travel_chart, turnip_chart

logger = logging.getLogger('gradiusbot')
logger.info("[Scheduled Task] <animal_crossing_tasks.py>: This runs the Animal Crossing background tasks.")

ac_manager = AcManager()


@asyncio.coroutine
async def action(client, config):
    while True:
        if client.is_ready():
            try:
                # display relevant chart information, if it's changed
                guild_id = config.getint('animalcrossing', 'server_id')
                channel_id = config.getint('animalcrossing', 'channel_id')
                target_guild = client.get_guild(guild_id)
                target_channel = client.get_channel(channel_id)

                user_list = ac_manager.user_list()
                chart = turnip_chart(user_list, target_guild)
                await target_channel.send(f"**Turnip Prices**\n```\n{chart}\n```")

                chart = travel_chart(user_list, target_guild)
                await target_channel.send(f"**Travel List**\n```\n{chart}\n```")

            except:
                logger.error(traceback.format_exc())

            # remove island setting if the island has been open for more than 24 hours
        await asyncio.sleep(5)
