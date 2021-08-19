import logging
from discord.ext import commands

# setup logging
logger = logging.getLogger("gradiusbot")


class DumbRole(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def dumbrole(self, ctx: commands.Context):
        """
        deletes dumb roles
        """
        count = 0
        for target_role in ctx.guild.roles:
            if target_role.name == 'ROLENAME':
                print("Bad role!", target_role.name)
                await target_role.delete()
                count += 1
        await ctx.send(f"Deleted {count} dumb roles.")


def setup(bot):
    bot.add_cog(DumbRole(bot))