from discord.ext import commands

class ButtonBuilder(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        print(interaction.data)
        print(interaction.message.id)