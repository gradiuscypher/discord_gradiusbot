# ref: https://discordpy.readthedocs.io/en/master/api.html?highlight=buttonstyle#bot-ui-kit
import discord
import logging
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
        if interaction.data['name'] == 'namecolor':
            if interaction.data['options'][0]['name'] == 'add':
                if 'resolved' in interaction.data.keys():
                    for role_id in interaction.data['resolved']['roles']:
                        if interaction.data['resolved']['roles'][role_id]['name'].split('_')[0] == 'namecolor':

                            old_role = None
                            # remove any old namecolor roles
                            for user_role in interaction.user.roles:
                                if 'namecolor_' in user_role.name:
                                    old_role = user_role
                                    await interaction.user.remove_roles(user_role)

                            # add the new namecolor and message the user
                            new_role = interaction.guild.get_role(int(role_id))

                            if new_role:
                                respose_embed = discord.Embed(color=discord.Color.green(), title="Enjoy your new name color!")
                                respose_embed.add_field(name="New Color", value=f"<@&{new_role.id}>")
                                if old_role:
                                    respose_embed.add_field(name="Old Color", value=f"<@&{old_role.id}>")

                                await interaction.user.add_roles(new_role)
                                await interaction.response.send_message(embeds=[respose_embed], ephemeral=True)
                            else:
                                respose_embed = discord.Embed(color=discord.Color.red(), title="Something went wrong, contact gradius")
                                await interaction.response.send_message(embeds=[respose_embed], ephemeral=True)

                        else:
                            respose_embed = discord.Embed(color=discord.Color.red(), title="You cannot grant yourself this role")
                            await interaction.response.send_message(embeds=[respose_embed], ephemeral=True)

            if interaction.data['options'][0]['name'] == 'clear':
                # remove any old namecolor roles
                for user_role in interaction.user.roles:
                    if 'namecolor_' in user_role.name:
                        old_role = user_role
                        await interaction.user.remove_roles(user_role)
                        respose_embed = discord.Embed(color=discord.Color.green(), title="Cleaned up your namecolors!")
                        await interaction.response.send_message(embeds=[respose_embed], ephemeral=True)



def setup(bot):
    bot.add_cog(ButtonBuilder(bot))