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


class Inventory:
    def __init__(self):
        self.items = {}

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

