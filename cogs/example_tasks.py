import logging

from discord.ext import commands, tasks

logger = logging.getLogger(__name__)


class ExampleTimer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.index = 0
        self.printer.start()
        self.bot = bot

    def cog_unload(self) -> None:
        self.printer.cancel()

    @tasks.loop(seconds=1.0)
    async def printer(self) -> None:
        async for guild in self.bot.fetch_guilds():
            logger.debug(guild)

        print(f"Current example task index: {self.index}")
        self.index += 1


async def setup(bot: commands.Bot) -> None:
    logger.info("Loading example Cog")
    await bot.add_cog(ExampleTimer(bot))
