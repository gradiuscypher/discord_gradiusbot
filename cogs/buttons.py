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

    @commands.command()
    async def build(self, ctx):
        """
        """
        view = discord.ui.View()
        button = discord.ui.Button(custom_id="1234", label="TestLabel", style=discord.ButtonStyle.blurple)
        button2 = discord.ui.Button(custom_id="9876", label="TestLabel2", style=discord.ButtonStyle.danger)
        view.add_item(button)
        view.add_item(button2)
        await ctx.send("Message", view=view)
    
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        print(interaction.data)


def setup(bot):
    bot.add_cog(ButtonBuilder(bot))