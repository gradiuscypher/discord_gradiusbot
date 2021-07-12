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
        if interaction.type == discord.InteractionType.application_command and interaction.data['name'] == 'namecolor':
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
                                response_embed = discord.Embed(color=discord.Color.green(), title="Enjoy your new name color!")
                                response_embed.add_field(name="New Color", value=f"<@&{new_role.id}>")
                                if old_role:
                                    response_embed.add_field(name="Old Color", value=f"<@&{old_role.id}>")

                                await interaction.user.add_roles(new_role)
                                await interaction.response.send_message(embeds=[response_embed], ephemeral=True)
                            else:
                                response_embed = discord.Embed(color=discord.Color.red(), title="Something went wrong, contact gradius")
                                await interaction.response.send_message(embeds=[response_embed], ephemeral=True)

                        else:
                            response_embed = discord.Embed(color=discord.Color.red(), title="You cannot grant yourself this role")
                            await interaction.response.send_message(embeds=[response_embed], ephemeral=True)

            if interaction.data['options'][0]['name'] == 'clear':
                # remove any old namecolor roles
                for user_role in interaction.user.roles:
                    if 'namecolor_' in user_role.name:
                        old_role = user_role
                        await interaction.user.remove_roles(user_role)
                        response_embed = discord.Embed(color=discord.Color.green(), title="Cleaned up your namecolors!")
                        await interaction.response.send_message(embeds=[response_embed], ephemeral=True)

            if interaction.data['options'][0]['name'] == 'list':
                # remove any old namecolor roles
                response_embed = discord.Embed(color=discord.Color.green(), title="Available Namecolors")
                response_body = ""

                for guild_role in interaction.guild.roles:
                    if 'namecolor_' in guild_role.name:
                        response_body += f"\n<@&{guild_role.id}>"

                response_embed.description = response_body
                await interaction.response.send_message(embeds=[response_embed], ephemeral=True)


def setup(bot):
    bot.add_cog(ButtonBuilder(bot))