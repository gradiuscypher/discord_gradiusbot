async def namecolor(**kwargs):
    attr_1 = kwargs['attr_1']
    attr_2 = kwargs['attr_2']
    interaction = kwargs['interaction']
    message = f"Running namecolor script {attr_1} {attr_2}"
    await interaction.response.send_message(message, ephemeral=True)


async def lootbox(**kwargs):
    interaction = kwargs['interaction']
    await interaction.response.send_message("LOOTBOX", ephemeral=False)
    print("LOOTBOX")