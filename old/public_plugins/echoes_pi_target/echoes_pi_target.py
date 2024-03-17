# TODO: calculate distance between gates: https://github.com/kaelspencer/everest
# TODO: https://everest.kaelspencer.com/jump/1C-953/G-0Q86/

import logging
import discord.utils
from discord import Embed, Color
from tabulate import tabulate
from libs.echoes import ee_libs

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <echoes_pi_target.py> Tracking for PI mining targets.")

help_str = """**Available Commands:**
```
!pp help - this command
!pp list - list all available Planetary Production items
!pp update <ITEM_LIST> - update the target Planetary Production list. Separate each item in <ITEM_LIST> with a comma.
```

**Example Update Command:**
```
!pp update nanites,dark compound,plasmoids
```
"""

product_strings = [
    "base metals",
    "condensates",
    "heavy water",
    "fiber composite",
    "smartfab units",
    "lustering alloy",
    "toxic metals",
    "coolant",
    "noble gas",
    "opulent compound",
    "silicate glass",
    "motley compound",
    "heavy metals",
    "reactive gas",
    "noble metals",
    "condensed alloy",
    "sheen compound",
    "supertensile plastics",
    "suspended plasma",
    "industrial fibers",
    "lucent compound",
    "liquid ozone",
    "polyaramids",
    "construction blocks",
    "reactive metals",
    "plasmoids",
    "gleaming alloy",
    "crystal compound",
    "glossy compound",
    "ionic solutions",
    "dark compound",
    "precious alloy",
    "oxygen isotopes",
    "nanites"
]


async def action(**kwargs):
    """
    :param kwargs:
    :return:
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    required_user_role = config.get('echoes', 'industry_role')
    in_industry_role = discord.utils.get(message.author.roles, name=required_user_role)

    split_content = message.content.split()

    if split_content[0] == '!pp' and in_industry_role:
        if split_content[1] == 'update':
            if len(split_content) >= 3:
                pi_targets = ' '.join(split_content[2:]).split(',')

                invalid_items = []
                valid_items = []
                for target_item in pi_targets:
                    target_item = target_item.lower().strip()

                    if target_item not in product_strings:
                        invalid_items.append(target_item)
                    else:
                        valid_items.append(target_item)

                if len(invalid_items) > 0:
                    status_embed = Embed(title="Planetary Production Corp Target - Update Failed", color=Color.red(),
                                         description="Some invalid items were found. List valid item names with `!pp list`")
                    status_embed.add_field(name="Valid Items", value="\n".join(valid_items), inline=False)
                    status_embed.add_field(name="Invalid Items", value="\n".join(invalid_items), inline=False)
                    await message.channel.send(embed=status_embed)

                else:
                    status_embed = Embed(title="Planetary Production Corp Target - Update", color=Color.green(),
                                         description="These are the Planetary Production items you should produce for the corporation")
                    status_embed.add_field(name="Needed Items", value="\n".join(valid_items), inline=False)

                    with open('echoes_pp_target_msg_id', 'r') as id_file:
                        old_id = id_file.read()
                        if old_id != '':
                            try:
                                old_message = await message.channel.fetch_message(int(old_id))
                                if old_message:
                                    await old_message.unpin()
                            except:
                                await message.channel.send("Unable to unpin old message. Please unpin manually.")

                    new_message = await message.channel.send(embed=status_embed)

                    for t_item in valid_items:
                        out_msg_list = []
                        best_locations = ee_libs.get_best_planets(t_item, max_locations=5)
                        for location in best_locations:
                            out_msg_list.append([location.jumps, location.planet, location.richness, location.output])
                        location_table = tabulate(out_msg_list, headers=["Jumps", "Planet", "Richness", "Output"])
                        await message.channel.send(f"**{t_item}**\n```\n{location_table}\n```")

                    await new_message.pin()
                    with open('echoes_pp_target_msg_id', 'w') as id_file:
                        id_file.write(str(new_message.id))

        if split_content[1] == 'list':
            item_embed = Embed(title="Planetary Production Corp Target - Item List", color=Color.green(),
                               description="This are the valid item names to include in your command. Separate each item with a comma.")
            item_embed.add_field(name="Valid Items", value="\n".join(product_strings), inline=False)
            await message.channel.send(embed=item_embed)

        if split_content[1] == 'help':
            await message.channel.send(help_str)
