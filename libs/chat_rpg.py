import pickle


class Game:
    def __init__(self):
        self.characters = {}

    def create_character(self, name):
        self.characters[name] = (Character(name))

    def get_character(self, name):
        if name in self.characters.keys():
            return self.characters[name]

    def save_game(self):
        pickle.dump(self.characters, open('data/character_db.dat', 'wb'))

    def load_game(self):
        self.characters = pickle.load(open('data/character_db.dat', 'rb'))


class Character:
    def __init__(self, name):
        self.inventory = Inventory()
        self.name = name
        self.xp = 0
        self.gear = {'head': None, 'chest': None, 'arms': None, 'hands': None, 'legs': None, 'feet': None,
                     'l_hand': None, 'r_hand': None}


class Inventory:
    def __init__(self):
        self.items = {}
        self.equipment = {}

    def add_item(self, item_id, count):
        if item_id in self.items.keys():
            self.items[item_id] = self.items[item_id] + count
        else:
            self.items[item_id] = count

    def remove_item(self, item_id, count):
        if item_id in self.items.keys():
            self.items[item_id] = self.items[item_id] - count


class Item:
    def __init__(self, item_id, name, cost):
        self.item_id = item_id
        self.name = name
        self.cost = cost


class ItemDb:
    def __init__(self):
        self.items = {}

    def create_item(self, item_id, name, cost):
        self.load_item_db()
        new_item = Item(item_id, name, cost)
        self.items[item_id] = new_item
        self.save_item_db()

    def delete_item(self, item_id):
        self.load_item_db()
        self.save_item_db()

    def get_item(self, item_id):
        self.load_item_db()
        if item_id in self.items.keys():
            return self.items[item_id]

    def item_exists(self, item_id):
        self.load_item_db()
        if item_id in self.items.keys():
            return True
        else:
            return False

    def load_item_db(self):
        self.items = pickle.load(open('data/item_db.dat', 'rb'))

    def save_item_db(self):
        pickle.dump(self.items, open('data/item_db.dat', 'wb'))


class Equipment:
    def __init__(self, equip_id, name, cost, slot, attack, defense):
        self.equip_id = equip_id
        self.name = name
        self.cost = cost
        self.slot = slot
        self.attack = attack
        self.defense = defense


class EquipDB:
    def __init__(self):
        self.equip = {}

    def create_equip(self, equip_id, name, cost, slot, attack, defense):
        self.load_equip_db()
        new_equip = Equipment(equip_id, name, cost, slot, attack, defense)
        self.equip[equip_id] = new_equip
        self.save_equip_db()

    def delete_equip(self, equip_id):
        self.load_equip_db()
        self.save_equip_db()

    def get_equip(self, equip_id):
        self.load_equip_db()
        if equip_id in self.equip.keys():
            return self.equip[equip_id]

    def equip_exists(self, equip_id):
        self.load_equip_db()
        if equip_id in self.equip.keys():
            return True
        else:
            return False

    def load_equip_db(self):
        self.equip = pickle.load(open('data/equip_db.dat', 'rb'))

    def save_equip_db(self):
        pickle.dump(self.equip, open('data/equip_db.dat', 'wb'))
