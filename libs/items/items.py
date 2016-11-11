"""
Basic item functions. Other packages could contain more specific item functions.
"""
from .basic import *


class Item:

    def action(self, client, config):
        return True

    def get_name(self):
        return "Name"

    def get_description(self):
        return "Description"

    def get_usage(self):
        return "Usage"

    def lookup_table(self, id):
        item_ids = {
            0: Dice
        }

        try:
            return item_ids[id]
        except:
            return None

