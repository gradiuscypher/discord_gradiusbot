import discord
import logging
import traceback
from discord.components import Button
import libs.scripts.items

from discord.ui import view
from libs.db.inventory import ItemManager, ItemInstance

# setup logging
logger = logging.getLogger("gradiusbot")

def split_to_pages(item_list, page_size=20):
    return [item_list[i:i+page_size] for i in range(0, len(item_list), page_size)]

def paged_button_view(item_list, page_size=20, target_page=0, button_length=30):
    view = discord.ui.View()
    paginated_list = split_to_pages(item_list, page_size=page_size)

    target_page = min(target_page, len(paginated_list)-1)

    # Add item list
    for item in paginated_list[target_page]:
        # TODO: can we get buttons to line up better?
        # buffered_name = (item.center(button_length, ' ')[:button_length]) if len(item) < button_length else item[:button_length-3]+'...'
        button = discord.ui.Button(custom_id=item.split(':')[1], label=item.split(':')[0], style=discord.ButtonStyle.blurple)
        button.callback = render_item_view
        view.add_item(button)

    # Add Navigation buttons
    button = discord.ui.Button(custom_id=f"prev_{target_page-1}", label="Prev", style=discord.ButtonStyle.green, row=4, disabled=(target_page-1 < 0))
    button.callback = update_inventory_view
    view.add_item(button)
    button = discord.ui.Button(custom_id=f"blank", label="    ", style=discord.ButtonStyle.grey, disabled=True, row=4)
    view.add_item(button)
    button = discord.ui.Button(custom_id=f"page_number", label=f"{target_page+1}/{len(paginated_list)}", style=discord.ButtonStyle.grey, disabled=True, row=4)
    view.add_item(button)
    button = discord.ui.Button(custom_id=f"blank", label="    ", style=discord.ButtonStyle.grey, disabled=True, row=4)
    view.add_item(button)
    button = discord.ui.Button(custom_id=f"next_{target_page+1}", label="Next", style=discord.ButtonStyle.green, row=4, disabled=(target_page+1 >= len(paginated_list)))
    button.callback = update_inventory_view
    view.add_item(button)

    return view


async def update_inventory_view(interaction):
    target_page = max(0, int(interaction.data['custom_id'].split('_')[1]))
    new_view = render_inventory_view(interaction.user.id, target_page=target_page)
    await interaction.response.edit_message(view=new_view)


def render_inventory_view(user_id, target_page=0):
    try:
        user_inven = ItemManager().get_inventory(user_id)
        item_list = [f"{i.count} x {i.item.name}:{i.id}" for i in user_inven.items]
        return paged_button_view(item_list, target_page=target_page)

    except:
        logger.error(traceback.format_exc())
        return None


async def render_item_view(interaction):
    item_instance = ItemInstance().get_item_instance(interaction.data['custom_id'])
    view = discord.ui.View()
    embed = discord.Embed(title=f'**{item_instance.item.name}**', description=f'{item_instance.item.description}')
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/413480748109004800/861111966175854622/box.png")

    if item_instance.item.usable:
        button = discord.ui.Button(custom_id=interaction.data['custom_id'], label="Use", style=discord.ButtonStyle.green, emoji='✔️')
        button.callback = run_item_script
        view.add_item(button)

    button = discord.ui.Button(custom_id=f"close_0", label="Back", style=discord.ButtonStyle.grey, disabled=False, emoji='👈')
    button.callback = update_inventory_view
    view.add_item(button)

    await interaction.response.edit_message(content="", view=view, embed=embed)


async def run_item_script(interaction):
    target_item = ItemInstance().get_item_instance(interaction.data['custom_id'])
    
    if target_item.item.usable:
        method = getattr(libs.scripts.items, target_item.item.script)
        await method(interaction=interaction)