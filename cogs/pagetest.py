# ref: https://discordpy.readthedocs.io/en/master/api.html?highlight=buttonstyle#bot-ui-kit
import discord
import logging
import random
from discord import components
from discord.enums import ButtonStyle
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
        styles = [
            discord.ButtonStyle.blurple,
            discord.ButtonStyle.primary,
            discord.ButtonStyle.secondary,
            discord.ButtonStyle.success,
            discord.ButtonStyle.danger,
            discord.ButtonStyle.grey,
            discord.ButtonStyle.green,
            discord.ButtonStyle.red
        ]
        view = discord.ui.View()
        short_button_text = "3000x Button Item"
        short_button_text2 = "3000x Button Item Length"
        short_button_text3 = "3000x Button Item Somewhat Longer"
        long_button_text = "15x Test item this is a very long description that should be long"

        texts = [
            # short_button_text,
            short_button_text2,
            # short_button_text3
        ]

        for num in range(0,20):
            button = discord.ui.Button(custom_id=f"id{num}", label=random.choice(texts), style=random.choice(styles))
            view.add_item(button)

        
        button = discord.ui.Button(custom_id=f"id{num}", label="Prev", style=discord.ButtonStyle.green)
        view.add_item(button)

        button = discord.ui.Button(custom_id=f"id{num}", label="    ", style=discord.ButtonStyle.grey, disabled=True)
        view.add_item(button)
        button = discord.ui.Button(custom_id=f"id{num}", label="4/15", style=discord.ButtonStyle.green, disabled=True)
        view.add_item(button)
        button = discord.ui.Button(custom_id=f"id{num}", label="    ", style=discord.ButtonStyle.grey, disabled=True)
        view.add_item(button)

        button = discord.ui.Button(custom_id=f"id{num}", label="Next", style=discord.ButtonStyle.green)
        view.add_item(button)


        await ctx.send(short_button_text, view=view)
    
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        print(interaction.data)


def setup(bot):
    bot.add_cog(ButtonBuilder(bot))