# Class responsible for managing loot
import sqlite3
import configparser
import random


class Loot:

    def __init__(self):
        self.connection = sqlite3.connect('loot.db')
        self.connection.row_factory = sqlite3.Row

        self.config = configparser.RawConfigParser()
        self.config.read('config.conf')

    def build_db(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE currency(user text, balance real)")
        self.connection.commit()

    def get_currency(self, target):
        cursor = self.connection.cursor()
        cursor.execute("select balance from currency where user=?", (target,))
        result = cursor.fetchone()

        if result is not None:
            return result['balance']
        else:
            cursor.execute("insert into currency values(?, 0)", (target,))
            return 0

    def add_currency(self, target, amount):
        current_balance = self.get_currency(target)

        new_balance = current_balance + amount

        cursor = self.connection.cursor()

        cursor.execute("update currency set balance=? where user=?", (new_balance, target))

        return new_balance

    def currency_chest(self, target):
        min_reward = self.config.getint("Loot", "chest_max_currency")
        max_reward = self.config.getint("Loot", "chest_min_currency")
        reward = random.randint(min_reward, max_reward)

        self.add_currency(target, reward)

        return target, reward
