import discord.utils
import logging
import os.path
import pickle
from discord import Interaction, ButtonStyle, Embed, Color 
from discord.ext import commands
from discord.ui import Button, View


logger = logging.getLogger("gradiusbot")


class RoleCtaButton(Button['RoleCtaView']):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def callback(self, interaction: Interaction):
        if interaction.data['custom_id'].startswith('cta_'):
            target_role_id = int(interaction.data['custom_id'].split('_')[1])
            target_role = interaction.guild.get_role(target_role_id)
            await interaction.user.add_roles(target_role)
            await interaction.response.send_message(f"You've successfully joined {target_role.name.replace('.', '')}", ephemeral=True)


class RoleCtaView(View):
    def __init__(self, target_role_id, *args, **kwargs):
        super().__init__()
        self.timeout = None

        # add the confirmation button
        self.add_item(RoleCtaButton(custom_id=f"cta_{target_role_id}", label="Join", style=ButtonStyle.blurple, emoji='🎉'))


class RoleCta(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == discord.InteractionType.application_command and interaction.data['name'] == 'cta':
            role_id = int(next(iter(interaction.data['resolved']['roles'])))
            target_role = interaction.guild.get_role(role_id)

            if target_role.name.startswith('.'):
                # check if our pickle of role cta exists
                if os.path.exists('role_cta.pickle'):
                    with open('role_cta.pickle', 'rb') as role_pickle:
                        role_cta_list = pickle.load(role_pickle)
                        role_cta_list.append(role_id)
                    with open('role_cta.pickle', 'wb') as role_pickle:
                        pickle.dump(role_cta_list, role_pickle)

                # if not, create it and add to it
                else:
                    with open('role_cta.pickle', 'wb') as role_pickle:
                        role_cta_list = [role_id]
                        pickle.dump(role_cta_list, role_pickle)

                view = RoleCtaView(role_id)
                cta_embed = Embed(title=f"Join - {target_role.name.replace('.', '')}", description=f"Click the button to join {target_role.name.replace('.','')}!", color=Color.blurple())
                await interaction.response.send_message(view=view, embed=cta_embed)
            else:
                await interaction.response.send_message("You cannot CTA that role.", ephemeral=True)


def setup(bot):
    bot.add_cog(RoleCta(bot))
