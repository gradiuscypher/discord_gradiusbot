# ref: https://discordpy.readthedocs.io/en/master/api.html?highlight=buttonstyle#bot-ui-kit
import discord
import logging
import random
from discord import components
from discord.enums import ButtonStyle
from discord.ext import commands
from libs import paginator

# setup logging
logger = logging.getLogger("gradiusbot")


class ButtonBuilder(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def build(self, ctx):
        """
        """
        styles = [
            discord.ButtonStyle.blurple,
            discord.ButtonStyle.primary,
            discord.ButtonStyle.secondary,
            discord.ButtonStyle.success,
            discord.ButtonStyle.danger,
            discord.ButtonStyle.grey,
            discord.ButtonStyle.green,
            discord.ButtonStyle.red
        ]
        view = discord.ui.View()
        short_button_text = "3000x Button Item"
        short_button_text2 = "3000x Button Item Length"
        short_button_text3 = "3000x Button Item Somewhat Longer"
        long_button_text = "15x Test item this is a very long description that should be long"

        texts = [
            # short_button_text,
            short_button_text2,
            # short_button_text3
        ]

        for num in range(0,15):
            button = discord.ui.Button(custom_id=f"id{num}", label=random.choice(texts), style=random.choice(styles))
            view.add_item(button)
        option_list = [
            discord.SelectOption(label='Select1', value='value_1', description='a longer description 11111', default=True),
            discord.SelectOption(label='Select2', value='value_2', description='a longer description 22222', default=False),
            discord.SelectOption(label='Select3', value='value_3', description='a longer description 33333', default=False)
        ]
        select = discord.ui.Select(custom_id="select", options=option_list)
        view.add_item(select)
        
        button = discord.ui.Button(custom_id=f"id{num}", label="Prev", style=discord.ButtonStyle.green)
        view.add_item(button)

        button = discord.ui.Button(custom_id=f"id{num}", label="    ", style=discord.ButtonStyle.grey, disabled=True)
        view.add_item(button)
        button = discord.ui.Button(custom_id=f"id{num}", label="4/15", style=discord.ButtonStyle.green, disabled=True)
        view.add_item(button)
        button = discord.ui.Button(custom_id=f"id{num}", label="    ", style=discord.ButtonStyle.grey, disabled=True)
        view.add_item(button)

        button = discord.ui.Button(custom_id=f"id{num}", label="Next", style=discord.ButtonStyle.green)
        view.add_item(button)


        await ctx.send(short_button_text, view=view)

    @commands.command()
    async def itemdemo(self, ctx):
        view = discord.ui.View()
        embed = discord.Embed(title='Test Item 123', description='This is the long form item description that you get.')
        option_list = [
            discord.SelectOption(label='Select1', value='value_1', description='a longer description 11111', default=False),
            discord.SelectOption(label='Select2', value='value_2', description='a longer description 22222', default=False),
            discord.SelectOption(label='Select3', value='value_3', description='a longer description 33333', default=False)
        ]
        embed.set_footer(text="This is the item footer.")
        embed.set_image(url='https://cdn.discordapp.com/attachments/353241001583837191/860381675661295616/unnamed_1.png')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/353241001583837191/860382001424760832/gradius_profile.jpg')
        embed.set_author(name="Author Name", url="https://www.google.com", icon_url='https://cdn.discordapp.com/attachments/353241001583837191/860382001424760832/gradius_profile.jpg')

        select = discord.ui.Select(custom_id="select", options=option_list, placeholder="Who are you trading with?")
        view.add_item(select)

        button = discord.ui.Button(custom_id=f"id_prev", label="Use", style=discord.ButtonStyle.green, emoji='✔️')
        view.add_item(button)

        button = discord.ui.Button(custom_id=f"id_blank", label="Trash", style=discord.ButtonStyle.red, disabled=False, emoji='🗑')
        view.add_item(button)
        button = discord.ui.Button(custom_id=f"id_page", label="Trade", style=discord.ButtonStyle.blurple, disabled=True, emoji='🤝')
        view.add_item(button)
        button = discord.ui.Button(custom_id=f"id_blank2", label="Store", style=discord.ButtonStyle.grey, disabled=False, emoji='📦')
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def pagetest(self, ctx):
        test_list = [f"ITEM_{num}" for num in range(0,80)]
        paginated_list = paginator.split_to_pages(test_list)
        page_view = paginator.paged_button_view(paginated_list, target_page=1)

        await ctx.send("Test", view=page_view)
    
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        print(interaction.data)
        print(interaction.message.id)


def setup(bot):
    bot.add_cog(ButtonBuilder(bot))