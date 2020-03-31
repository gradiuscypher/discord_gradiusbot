# TODO: implement the ac_libs versions of each function, remove pickle code

import asyncio
import logging
import os.path
import pickle
import traceback
from datetime import datetime
from libs.ac_libs import AcManager, AcUser, DiscordServer, TurnipEntry

logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <animal_crossing.py> Provides tools for the game Animal Crossing.")


help_str = """Here's how to use the Animal Crossing bot, all commands start with `!ac`:

Optional input is surrounded by `[]`, required input is surrounded by `<>`. Please do not include the `[]<>` symbols, though.
```
DM COMMANDS:
!ac help - this command.
!ac turnip add <PRICE> - set the current price that Turnips are for on your island. On Sundays this will be the buy price, all other days will be the sell price.
!ac friendcode <FRIEND CODE> - set your Nintendo friend code if you'd like others to be able to add you.
!ac island open [DODO CODE] - set your island to appear as open on the status chart. Include the DODO CODE if you'd like anyone to be able to join you.
!ac island close - set your island to appear as closed on the status chart.
!ac fruit <apple, pear, cherry, peach, orange> - set your native fruit for the status chart. Please use the names listed.

CHANNEL COMMANDS:
!ac stonks - show the turnip prices that have been registered
!ac social - show the friend codes that have been registered
!ac travel - show the islands that are open for travel and the native fruits
```
"""


def load_pickle(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'rb') as ac_pickle:
            ac_data = pickle.load(ac_pickle)
            return ac_data
    else:
        return {
            "users": {},
            "turnips": []
        }


def save_pickle(save_data, file_name):
    try:
        with open(file_name, 'wb') as ac_pickle:
            pickle.dump(save_data, ac_pickle)
        return True

    except:
        logger.error(traceback.format_exc())
        return False


@asyncio.coroutine
async def action(**kwargs):
    """
    Functions:
        turnip price (if sunday, buy price, otherwise sell price)
        turnip chart (show a chart of registered turnip prices)
        friendcode
        fruit
        island open
        island close
    :param kwargs:
    :return:
    """
    message = kwargs['message']
    config = kwargs['config']

    split_msg = message.content.split()
    sender_id = message.author.id

    if split_msg[0] == '!ac' and len(split_msg) == 1:
        await message.channel.send(help_str)

    elif split_msg[0] == '!ac' and len(split_msg) > 1:

        if split_msg[1] == 'turnip':
            if split_msg[2] == 'add' and len(split_msg) == 4:
                try:
                    turnip_price = int(split_msg[3])
                    success = add_turnip(config, sender_id, turnip_price)

                    if success:
                        await message.add_reaction("🆗")
                    else:
                        await message.add_reaction("❌")
                        logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
                except:
                    await message.add_reaction("❌")
                    logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
                    logger.error(traceback.format_exc())

        elif split_msg[1] == 'friendcode' and len(split_msg) == 3:
            friendcode = split_msg[2]

            try:
                success = set_friendcode(config, sender_id, friendcode)

                if success:
                    await message.add_reaction("🆗")
                else:
                    await message.add_reaction("❌")
                    logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")

            except:
                await message.add_reaction("❌")
                logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
                logger.error(traceback.format_exc())

        elif split_msg[1] == 'fruit' and len(split_msg) == 3:
            target_fruit = split_msg[2]
            fruit_list = ['apple', 'pear', 'cherry', 'peach', 'orange']

            if target_fruit in fruit_list:
                success = set_fruit(config, sender_id, target_fruit)

                if success:
                    await message.add_reaction("🆗")
                else:
                    await message.add_reaction("❌")
                    logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
            else:
                await message.add_reaction("❌")
                logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
                await message.channel.send(f"That fruit does not exist, please choose from the following: {fruit_list}")

        elif split_msg[1] == 'island':
            success = False

            if split_msg[2] == 'open':
                if len(split_msg) == 3:
                    success = set_island(config, sender_id, True)
                if len(split_msg) == 4:
                    dodo_code = split_msg[3]
                    success = set_island(config, sender_id, True, dodo_code=dodo_code)

            elif split_msg[2] == 'close':
                if len(split_msg) == 3:
                    success = set_island(config, sender_id, False, dodo_code='')

            if success:
                await message.add_reaction("🆗")
            else:
                await message.add_reaction("❌")
                logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
        elif split_msg[1] == 'help':
            await message.channel.send(help_str)

        else:
            await message.channel.send("You did not provide a properly formatted command. Check out !ac help for more info.")
            logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")


def add_turnip(config, discord_id, turnip_price):
    """
    Adds the most current turnip price to the users data and saves the old value to historical data
    :param config:
    :param discord_id:
    :param turnip_price:
    :return:
    """
    # load the most current pickle data
    pickle_file = config.get("animalcrossing", "pickle_file")
    ac_data = load_pickle(pickle_file)

    try:
        if discord_id in ac_data['users'].keys():
            user = ac_data['users'][discord_id]
            hist_turnips = ac_data['turnips']

            # save old turnip price to historical data
            hist_turnips.append({'discord_id': discord_id, 'price': user['turnip_price'], 'time': user['turnip_time']})

            # set new values to userdict
            user['turnip_price'] = turnip_price
            user['turnip_time'] = datetime.now()

            # save the data pickle
            save_pickle(ac_data, pickle_file)

            return True

        else:
            ac_data['users'][discord_id] = {
                'friend_code': '',
                'fruit': '',
                'island': False,
                'turnip_price': turnip_price,
                'turnip_time': datetime.now(),
                'dodo_code': ''
            }

            # save the data pickle
            save_pickle(ac_data, pickle_file)

            return True

    except:
        logger.error(traceback.format_exc())
        return False


def set_friendcode(config, discord_id, friendcode):
    """
    Sets the friendcode for the discord ID
    :param config:
    :param discord_id:
    :param friendcode:
    :return:
    """
    # load the most current pickle data
    pickle_file = config.get("animalcrossing", "pickle_file")
    ac_data = load_pickle(pickle_file)

    try:
        if discord_id in ac_data['users'].keys():
            ac_data['users'][discord_id]['friend_code'] = friendcode
            save_pickle(ac_data, pickle_file)
            return True

        else:
            ac_data['users'][discord_id] = {
                'friend_code': friendcode,
                'fruit': '',
                'island': False,
                'turnip_price': None,
                'turnip_time': None,
                'dodo_code': ''
            }

            # save the data pickle
            save_pickle(ac_data, pickle_file)

            return True
    except:
        logger.error(traceback.format_exc())
        return False


def set_fruit(config, discord_id, fruit):
    """
    Sets the fruit for the discord ID
    :param config:
    :param discord_id:
    :param fruit:
    :return:
    """
    # load the most current pickle data
    pickle_file = config.get("animalcrossing", "pickle_file")
    ac_data = load_pickle(pickle_file)

    try:
        if discord_id in ac_data['users'].keys():
            ac_data['users'][discord_id]['fruit'] = fruit
            save_pickle(ac_data, pickle_file)
            return True

        else:
            ac_data['users'][discord_id] = {
                'friend_code': '',
                'fruit': fruit,
                'island': False,
                'turnip_price': None,
                'turnip_time': None,
                'dodo_code': ''
            }

            # save the data pickle
            save_pickle(ac_data, pickle_file)

            return True
    except:
        logger.error(traceback.format_exc())
        return False


def set_island(config, discord_id, island_open, dodo_code=''):
    """
    Sets the boolean whether the Island is open or not.
    :param config:
    :param discord_id:
    :param island_open:
    :param dodo_code:
    :return:
    """
    # load the most current pickle data
    pickle_file = config.get("animalcrossing", "pickle_file")
    ac_data = load_pickle(pickle_file)

    try:
        if discord_id in ac_data['users'].keys():
            ac_data['users'][discord_id]['island'] = island_open
            ac_data['users'][discord_id]['dodo_code'] = dodo_code
            save_pickle(ac_data, pickle_file)
            return True

        else:
            ac_data['users'][discord_id] = {
                'friend_code': '',
                'fruit': '',
                'island': island_open,
                'turnip_price': None,
                'turnip_time': None,
                'dodo_code': dodo_code
            }

            # save the data pickle
            save_pickle(ac_data, pickle_file)

            return True
    except:
        logger.error(traceback.format_exc())
        return False
