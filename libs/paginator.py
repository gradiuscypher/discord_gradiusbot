import discord

def split_to_pages(item_list, page_size=20):
    return [item_list[i:i+page_size] for i in range(0, len(item_list), page_size)]

def paged_button_view(paginated_list, target_page=0, button_length=30):
    view = discord.ui.View()

    # Add item list
    for item in paginated_list[target_page]:
        # TODO: can we get buttons to line up better?
        # buffered_name = (item.center(button_length, ' ')[:button_length]) if len(item) < button_length else item[:button_length-3]+'...'
        button = discord.ui.Button(custom_id=item, label=item, style=discord.ButtonStyle.blurple)
        view.add_item(button)

    # Add Navigation buttons
    button = discord.ui.Button(custom_id=f"prev", label="Prev", style=discord.ButtonStyle.green, row=4)
    view.add_item(button)
    button = discord.ui.Button(custom_id=f"blank", label="    ", style=discord.ButtonStyle.grey, disabled=True, row=4)
    view.add_item(button)
    button = discord.ui.Button(custom_id=f"page_number", label=f"{target_page+1}/{len(paginated_list)}", style=discord.ButtonStyle.green, disabled=True, row=4)
    view.add_item(button)
    button = discord.ui.Button(custom_id=f"blank", label="    ", style=discord.ButtonStyle.grey, disabled=True, row=4)
    view.add_item(button)
    button = discord.ui.Button(custom_id=f"next", label="Next", style=discord.ButtonStyle.green, row=4)
    view.add_item(button)

    return view