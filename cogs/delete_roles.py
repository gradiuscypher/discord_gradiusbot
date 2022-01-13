import discord
import logging
from discord.ext import commands

# setup logging
logger = logging.getLogger("gradiusbot")


class DumbRoles(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def clean(self, ctx, *, input):
        """
        Echoes the message
        """
        # await ctx.send(input)
        roles = ctx.guild.roles
        for role in roles:
            if role.name == 'XMETA':
                print("Deleting role.")
                await role.delete()


def setup(bot):
    bot.add_cog(DumbRoles(bot))
