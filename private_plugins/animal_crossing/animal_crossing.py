import asyncio
import logging
import os.path
import pickle
import traceback
from datetime import datetime
from tabulate import tabulate

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <animal_crossing.py> Provides tools for the game Animal Crossing.")

"""
ac_data layout:
{
    "users": {"discord_id":
        {
            "friendcode": STR:FRIEND CODE,
            "fruit": STR:FRUIT NAME
            "island": BOOL:ISLAND OPEN STATUS
            "turnip_price": INT:BELL PRICE,
            "turnip_time": DATETIME: TIME INPUTTED
        }
    },
    "turnips": [
        {
            "discord_id": INT:DISCORD ID,
            "price": INT:BELL PRICE,
            "time": DATETIME: TIME INPUTTED
        }
    ]
}
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
    client = kwargs['client']

    split_msg = message.content.split()
    sender_id = message.author.id

    if split_msg[0] == '!ac':

        if split_msg[1] == 'turnip':
            if split_msg[2] == 'add' and len(split_msg) == 4:
                try:
                    turnip_price = int(split_msg[3])
                    success = add_turnip(config, sender_id, turnip_price)

                    if success:
                        await message.add_reaction("🆗")
                    else:
                        await message.add_reaction("❌")
                except:
                    await message.add_reaction("❌")
                    logger.error(traceback.format_exc())

        elif split_msg[1] == 'friendcode' and len(split_msg) == 3:
            friendcode = split_msg[2]

            try:
                success = set_friendcode(config, sender_id, friendcode)

                if success:
                    await message.add_reaction("🆗")
                else:
                    await message.add_reaction("❌")

            except:
                await message.add_reaction("❌")
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
            else:
                await message.add_reaction("❌")
                await message.channel.send(f"That fruit does not exist, please choose from the following: {fruit_list}")

        elif split_msg[1] == 'island':
            success = False

            if split_msg[2] == 'open' and len(split_msg) == 3:
                success = set_island(config, sender_id, True)
            elif split_msg[2] == 'close' and len(split_msg) == 3:
                success = set_island(config, sender_id, False)

            if success:
                await message.add_reaction("🆗")
            else:
                await message.add_reaction("❌")

        elif split_msg[1] == 'chart':
            chart = build_chart(config, message.guild)
            await message.channel.send(f"```\n{chart}\n```")


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
                'turnip_time': datetime.now()
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
                'turnip_time': None
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
                'turnip_time': None
            }

            # save the data pickle
            save_pickle(ac_data, pickle_file)

            return True
    except:
        logger.error(traceback.format_exc())
        return False


def set_island(config, discord_id, island_open):
    """
    Sets the boolean whether the Island is open or not.
    :param config:
    :param discord_id:
    :param island_open:
    :return:
    """
    # load the most current pickle data
    pickle_file = config.get("animalcrossing", "pickle_file")
    ac_data = load_pickle(pickle_file)

    try:
        if discord_id in ac_data['users'].keys():
            ac_data['users'][discord_id]['island'] = island_open
            save_pickle(ac_data, pickle_file)
            return True

        else:
            ac_data['users'][discord_id] = {
                'friend_code': '',
                'fruit': '',
                'island': island_open,
                'turnip_price': None,
                'turnip_time': None
            }

            # save the data pickle
            save_pickle(ac_data, pickle_file)

            return True
    except:
        logger.error(traceback.format_exc())
        return False


def build_chart(config, guild):
    # load the most current pickle data
    pickle_file = config.get("animalcrossing", "pickle_file")
    ac_data = load_pickle(pickle_file)

    out_table = []
    fruit_list = ['apple', 'pear', 'cherry', 'peach', 'orange']
    fruit_lookup = {'apple': '🍎', 'pear': '🍐', 'cherry': '🍒', 'peach': '🍑', 'orange': '🍊'}

    for discord_user in ac_data['users']:
        discord_name = guild.get_member(discord_user).display_name
        friend_code = ac_data['users'][discord_user]['friend_code']
        island_open = '👍' if ac_data['users'][discord_user]['island'] else '👎'
        fruit = fruit_lookup[ac_data['users'][discord_user]['fruit']]

        t_price = ac_data['users'][discord_user]['turnip_price']
        t_time = ac_data['users'][discord_user]['turnip_time'].strftime("%b %d %H:%M")

        out_table.append([discord_name, friend_code, island_open + fruit, t_price, t_time])

    return tabulate(out_table, headers=['User', 'Friend Code', '🏝️', 'Turnip 🔔', 'Turnip ⏲️'])
