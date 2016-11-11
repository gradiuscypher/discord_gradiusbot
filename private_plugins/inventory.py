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

    if split_content[0] == "!item":

        if len(split_content) == 1:
            inventory_string = "```Your Inventory\n" \
                               "==============\n".format(message.author.name)
            inv_index = 1
            for item in items:
                item_details = item_manager.get_item_details(item.item_id)
                inventory_string += "{}) {} - {} : {}\n".format(inv_index, item_details['name'],
                                                                item_details['description'],
                                                                item_details['use'])
                inv_index += 1
            inventory_string += "```"
            yield from client.send_message(message.channel, inventory_string)

        if len(split_content) == 3:
            if split_content[1] == "use":
                item_index = int(split_content[2]) - 1
                yield from item_manager.get_item_details(items[item_index].id)[item_index]['function'](client, message, config)
