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
        if interaction.data['name'] == 'demo':
            await interaction.response.send_message("This is a demo slash command.", ephemeral=True)

        if interaction.data['name'] == 'options':
            resp = ""
            # process the multiple choice
            ephemeral= False

            for option_data in interaction.data['options']:
                if option_data['name'] == 'choicelist':
                    resp += f"\nchoice: {option_data['value']}"
                if option_data['name'] == 'freeform':
                    resp += f"\nfreeform:{option_data['value']}"
                if option_data['name'] == 'ephemeral':
                    ephemeral = option_data['value']
                    resp += f"\nephemeral:{option_data['value']}"

            await interaction.response.send_message(resp, ephemeral=ephemeral)


def setup(bot):
    bot.add_cog(ButtonBuilder(bot))