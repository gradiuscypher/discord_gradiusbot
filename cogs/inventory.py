# import discord.utils
# from discord.enums import ChannelType
# from discord import Embed, Color
# import libs.scripts.examples
# import logging

# logger = logging.getLogger('gradiusbot')

# logger.info("[Public Plugin] <example_script_plugin.py> An example of how plugins can run separate scripts.")


# async def action(**kwargs):
#     """
#     :param kwargs:
#     :return:
#     """
#     message = kwargs['message']
#     config = kwargs['config']
#     client = kwargs['client']

#     # ref: https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
#     if message.content == 'run plugin':
#         method = getattr(libs.scripts.examples, 'example_action_1')
#         await method(message=message)

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