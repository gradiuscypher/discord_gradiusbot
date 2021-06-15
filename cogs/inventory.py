# ref: https://discordpy.readthedocs.io/en/master/api.html?highlight=buttonstyle#bot-ui-kit
import discord
import logging
import libs.scripts.items
from discord import components
from discord import embeds
from discord.ext import commands

# setup logging
logger = logging.getLogger("gradiusbot")


class ButtonBuilder(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.data['name'] == 'inventory':
            # method = getattr(libs.scripts.items, 'namecolor')
            # await method(attr_1="Attr1", attr_2=2, interaction=interaction)
            if interaction.data['options'][0]['name'] == 'list':
                print("list")
                print(interaction.data)

            if interaction.data['options'][0]['name'] == 'use':
                print("use")
                print(interaction.data)



def setup(bot):
    bot.add_cog(ButtonBuilder(bot))