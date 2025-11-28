import discord
from discord import app_commands
from discord.ext import commands


class ExampleCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="example", description="An example ping!")
    async def example_command(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("This is an example command!")

    @app_commands.command(name="greet", description="Greet someone")
    @app_commands.describe(user="The user to greet")
    async def greet(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
    ) -> None:
        await interaction.response.send_message(f"Hello {user.mention}!")


async def setup(bot: commands.Bot) -> None:
    print("Loading example Cog")
    await bot.add_cog(ExampleCog(bot))
