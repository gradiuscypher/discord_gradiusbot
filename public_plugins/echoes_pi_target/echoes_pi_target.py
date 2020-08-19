# TODO: calculate distance between gates: https://github.com/kaelspencer/everest
# TODO: https://everest.kaelspencer.com/jump/1C-953/G-0Q86/

from discord import Embed, Color
import logging

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

    split_content = message.content.split()

    if split_content[0] == '!pp':
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
