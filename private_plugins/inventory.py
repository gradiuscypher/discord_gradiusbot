from libs.items.inventory import Inventory
from libs.items.items import Item
import asyncio

print("[Private Plugin] <inventory.py>: This plugin manages the user's inventory.")
help_message = """
__**!wallet help** (PM Only)__

Your GradiusCoin wallet. Collect GradiusCoin, spend GradiusCoin, give GradiusCoin.

Examples:
!wallet

Show your wallet balance.


"""

inventory_manager = Inventory()
item_manager = Item()


@asyncio.coroutine
def action(message, client, config):
    sender = message.author.id
    content = message.content
    split_content = content.split()
    items = inventory_manager.get_items(sender)

    if split_content[0] == "!inventory":
        inventory_string = "{} Inventory\n" \
                           "==========\n".format(message.author.name)
        for item in items:
            item_details = item_manager.get_item_details(item.id)
            inventory_string += "{} : {}\n".format(item_details['name'], item_details['description'])

        yield from client.send_message(message.channel, inventory_string)

        if len(split_content) == 3:
            item_index = int(split_content[2])
            if split_content[1] == "use":
                item_out = item_manager.get_item_details(items[item_index].id)['function']()
                yield from client.send_message(message.channel, "DICE ROLL {}".format(item_out))
