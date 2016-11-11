import random


class Dice:

    @staticmethod
    def get_name():
        return "die"

    @staticmethod
    def get_description():
        return "A 20 sided die."

    @staticmethod
    def get_usage():
        return "Rolls a 20 sided die."

    @staticmethod
    def action(client=None, config=None):
        return random.randint(1, 20)
