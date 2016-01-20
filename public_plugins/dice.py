import random
import asyncio

print("[Public Plugin] <dice.py>: This plugin rolls dice.")


@asyncio.coroutine
def action(message, client, config):
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

                yield from client.send_message(message.channel, "Your " + str(dice_count) + "d" + str(dice_value) + " rolled " + str(rolls) + " and your total is " + str(sum(rolls)))
                yield from client.delete_message(message)
            except:
                print("error")
                pass
