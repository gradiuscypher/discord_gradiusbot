import discord.utils
import logging
import traceback
from config import role_metadata
from discord import Interaction, SelectOption, ButtonStyle, Embed, Color
from discord.ext import commands
from discord.ui import Button, Select, View


logger = logging.getLogger("gradiusbot")


class WoweSelectorButton(Button['WoweSelectorView']):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        select_menu = discord.utils.get(self.view.children, custom_id='select_menu')
        selected_values = [int(option) for option in select_menu.values]
        # TODO: I wonder if this could be done more efficently with python sets
        unselected_values = [option.value for option in select_menu.options if option.value not in selected_values]
        added_roles = []
        removed_roles = []

        thinking_embed = Embed(color=Color.yellow(), title="Thinking...", description="Currwentwy prowcessing your reqwuest. Pweese hold tight!")
        thinking_embed.set_image(url='https://tenor.com/view/uwu-groove-vibe-dance-rainbow-gif-17715604')
        thinking_embed.set_footer(text="dis could be a widdle while, dere might be a wadda wowes...")
        await interaction.edit_original_message(embed=thinking_embed, view=None)

        try:
            # add selected roles
            for role_id in selected_values:
                target_role = interaction.guild.get_role(role_id)
                if target_role and target_role.name.startswith('.'):
                    await interaction.user.add_roles(interaction.guild.get_role(role_id))
                    added_roles.append(target_role)

            # remove unselected roles
            for role_id in unselected_values:
                target_role = interaction.guild.get_role(role_id)
                if target_role and target_role.name.startswith('.'):
                    await interaction.user.remove_roles(interaction.guild.get_role(role_id))
                    removed_roles.append(target_role)
            
            # report success
            embed_message = Embed(color=Color.green(), title='Successfuwy mawdiefied your wowes')
            embed_message.set_image(url="https://tenor.com/view/uwu-wink-gif-13867259")

            if len(added_roles) > 0:
                role_string = ''
                for role in added_roles:
                    role_name = f"{role.name.replace('.', '')}"
                    role_string += role_name + '\n'
                embed_message.add_field(name='== Enabled Wowes ==', value=role_string)

            if len(removed_roles) > 0:
                role_string = ''
                for role in removed_roles:
                    role_name = f"{role.name.replace('.', '')}"
                    role_string += role_name + '\n'
                embed_message.add_field(name='== Disabled Wowes ==', value=role_string)

            await interaction.edit_original_message(embed=embed_message, view=None, content='**Wowe Manager**')

        except:
            logger.error(traceback.format_exc())

            # report fail
            embed_message = Embed(color=Color.red(), title='Oopsie Woopsie!', description='We did a fucky wucky! Pweese let gwadius know something bwoke with the Wowe Sewector')
            await interaction.edit_original_message(embed=embed_message, view=None, content='**Wowe Manager**')


class WoweSelectorSelect(Select['WoweSelectorView']):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_values = len(self.options)
        self.min_values = 0
        self.custom_id = 'select_menu'


class WoweSelectorView(View):
    def __init__(self, target_roles, user_roles, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = None
        
        # create the option list from roles in the server that start with .
        option_list = []
        for role in target_roles:
            if role.name.startswith('.'):
                role_name = f'{role.name.replace(".", "")}'
                description_string = ("[Pingable] " if role.mentionable else "")
                description_string += role_metadata[role_name.lower()] if role_name.lower() in role_metadata.keys() else ""
                option_list.append(SelectOption(label=role_name, value=role.id, default=role in user_roles, description=description_string))
        self.selector = WoweSelectorSelect(options=option_list)
        self.add_item(self.selector)

        # add the confirmation button
        self.add_item(WoweSelectorButton(custom_id="custom_id", label="Confirm Wowes", style=ButtonStyle.green))


class WoweSelector(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == discord.InteractionType.application_command and interaction.data['name'] == 'wowes':
            view = WoweSelectorView(interaction.guild.roles, interaction.user.roles)
            await interaction.response.send_message("**Wowe Manager**", view=view, ephemeral=True)


def setup(bot):
    bot.add_cog(WoweSelector(bot))