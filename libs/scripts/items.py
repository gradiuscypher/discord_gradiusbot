async def namecolor(**kwargs):
    interaction = kwargs['interaction']
    message = f"Running namecolor script"
    await interaction.response.send_message(message, ephemeral=True)


async def lootbox(**kwargs):
    interaction = kwargs['interaction']
    await interaction.response.send_message("LOOTBOX", ephemeral=True)