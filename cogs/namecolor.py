# ref: https://discordpy.readthedocs.io/en/master/api.html?highlight=buttonstyle#bot-ui-kit
import discord
import logging
from discord import components
from discord.ext import commands

# setup logging
logger = logging.getLogger("gradiusbot")


class ButtonBuilder(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        print(interaction.data)
        if interaction.data['name'] == 'namecolor':
            await interaction.response.send_message("namecolor", ephemeral=True)


def setup(bot):
    bot.add_cog(ButtonBuilder(bot))