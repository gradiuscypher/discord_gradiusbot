import random
import asyncio


def dice_action(client=None, message=None, config=None):
    roll = random.randint(1, 20)
    yield from client.send_message(message.channel, "Dice roll: {}".format(roll))
