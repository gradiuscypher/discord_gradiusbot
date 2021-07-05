from os import name
import discord
from discord import guild


async def namecolor(**kwargs):
    interaction = kwargs['interaction']
    view = discord.ui.View()
    embed = discord.Embed(title='**Name Color Switcher**', description="Lets you pick a random name color from a list of colors.")
    message = ""

    namecolor_options = []
    for guild_role in interaction.guild.roles:
        if 'namecolor_' in guild_role.name:
            namecolor_options.append(discord.SelectOption(label=guild_role.name, value=guild_role.name, default=False))

    select = discord.ui.Select(custom_id="select", options=namecolor_options, placeholder="Which color would you like?")
    view.add_item(select)

    button = discord.ui.Button(custom_id="confirm", label="Confirm", style=discord.ButtonStyle.green, emoji='✔️')
    button.callback = modify_namecolor
    view.add_item(button)
    button = discord.ui.Button(custom_id="random", label="Randomize", style=discord.ButtonStyle.blurple, disabled=False, emoji='🎲')
    button.callback = modify_namecolor
    view.add_item(button)
    button = discord.ui.Button(custom_id="clear", label="Clear", style=discord.ButtonStyle.gray, disabled=False, emoji='🧹')
    button.callback = modify_namecolor
    view.add_item(button)
    button = discord.ui.Button(custom_id="cancel", label="Cancel", style=discord.ButtonStyle.red, disabled=False, emoji='🗑')
    button.callback = modify_namecolor
    view.add_item(button)

    await interaction.response.edit_message(content=message, view=view, embed=embed)


async def modify_namecolor(interaction):
    print(dir(interaction.original_message()))


async def lootbox(**kwargs):
    interaction = kwargs['interaction']
    await interaction.response.send_message("LOOTBOX", ephemeral=True)