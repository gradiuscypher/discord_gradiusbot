import asyncio
import logging
import pickle
import traceback
import os.path

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <animal_crossing.py> Provides tools for the game Animal Crossing.")

"""
ac_data layout:
{
    "users": [
        {
            "discord_id": INT:DISCORD ID,
            "friendcode": STR:FRIEND CODE,
            "fruit": STR:FRUIT NAME
            "island": BOOL:ISLAND OPEN STATUS
        }
    ],
    "turnips": [
        {
            "discord_id": INT:DISCORD ID,
            "price": INT:BELL PRICE,
            "time": DATETIME: TIME INPUTTED
        }
    ]
}
"""


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

    # load the most current pickle data
    ac_data = load_pickle()

    split_msg = message.content.split()

    if split_msg[0] == '!ac':

        if split_msg[1] == 'turnip':
            if split_msg[2] == 'add':
                pass
            elif split_msg[2] == 'chart':
                pass

        elif split_msg[1] == 'friendcode':
            pass

        elif split_msg[1] == 'fruit':
            pass

        elif split_msg[1] == 'island':
            if split_msg[2] == 'open':
                pass
            elif split_msg[2] == 'close':
                pass


def load_pickle():
    if os.path.exists('public_plugins/animal_crossing/data.pickle'):
        with open('public_plugins/animal_crossing/data.pickle', 'rb') as ac_pickle:
            ac_data = pickle.load(ac_pickle)
            return ac_data
    else:
        return {
            "users": [],
            "turnips": []
        }


def save_pickle(ac_data):
    try:
        with open('public_plugins/animal_crossing/data.pickle', 'wb') as ac_pickle:
            pickle.dump(ac_data, ac_pickle)
        return True

    except:
        logger.error(traceback.format_exc())
        return False
