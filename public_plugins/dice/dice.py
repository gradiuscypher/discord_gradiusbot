import random
import asyncio
import logging


logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <dice.py>: This plugin rolls dice.")


@asyncio.coroutine
async def action(message, config):
    split_content = message.content.split()
    rolls = []

    if split_content[0] == "!roll":
        if len(split_content) > 1:
            try:
                dice_str = split_content[1]
                dice_count = int(dice_str.split('d')[0])
                dice_value = int(dice_str.split('d')[1])

                for roll in range(0, dice_count):
                    rolls.append(random.randint(1, dice_value))

                await message.channel.send("Your " + str(dice_count) + "d" + str(dice_value) + " rolled " + str(rolls) + " and your total is " + str(sum(rolls)))
            except:
                print("error")
                pass
