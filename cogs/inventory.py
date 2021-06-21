# ref: https://discordpy.readthedocs.io/en/master/api.html?highlight=buttonstyle#bot-ui-kit
import discord
import logging
import libs.scripts.items
from libs.db.inventory import ItemManager
from discord import components
from discord import embeds
from discord.ext import commands


# setup logging
logger = logging.getLogger("gradiusbot")

# message strings
NO_SUCH_ITEM = "Either you do not have this item, or it does not exist."
NOT_USABLE = "This item is not usable."


class Inventory(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.data['name'] == 'inventory':
            if interaction.data['options'][0]['name'] == 'list':
                user_inven = ItemManager().get_inventory(interaction.user.id)

                if user_inven:
                    inven_string = "```\nInventory\n"
                    for i in user_inven.items:
                        inven_string += f"\n{i.count} {i.item.name} {i.item.description}"
                    inven_string += "\n```"
                    await interaction.response.send_message(inven_string, ephemeral=True)
                else:
                    logger.error(f"Failed to create/find inventory for user {interaction.user.id}")
                    await interaction.response.send_message("Looks like there was an error")

            if interaction.data['options'][0]['name'] == 'use':
                target_item_id = interaction.data['options'][0]['options'][0]['value'].upper()
                user_inven = ItemManager().get_inventory(interaction.user.id)
                target_item = user_inven.get_inventory_item(target_item_id)

                if target_item and target_item.count > 0:
                    if target_item.item.usable:
                        method = getattr(libs.scripts.items, target_item.item.script)
                        await method(attr_1="Attr1", attr_2=2, interaction=interaction)
                    else:
                        await interaction.response.send_message(NOT_USABLE, ephemeral=True)
                else:
                    await interaction.response.send_message(NO_SUCH_ITEM, ephemeral=True)


def setup(bot):
    bot.add_cog(Inventory(bot))