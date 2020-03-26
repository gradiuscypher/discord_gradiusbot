# TODO: highlight the highest / lowest price for turnips in the chart

import asyncio
import logging
import os.path
import pickle
import traceback
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

help_str = """Here's how to use the Animal Crossing bot, all commands start with `!ac`:

Optional input is surrounded by `[]`, required input is surrounded by `<>`. Please do not include the `[]<>` symbols, though.
```
!ac help - this command.
!ac turnip add <PRICE> - set the current price that Turnips are for on your island. On Sundays this will be the buy price, all other days will be the sell price.
!ac friendcode <FRIEND CODE> - set your Nintendo friend code if you'd like others to be able to add you.
!ac island open [DODO CODE] - set your island to appear as open on the status chart. Include the DODO CODE if you'd like anyone to be able to join you.
!ac island close - set your island to appear as closed on the status chart.
!ac fruit <apple, pear, cherry, peach, orange> - set your native fruit for the status chart. Please use the names listed.
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
    if split_msg[0] == '!ac' and len(split_msg) > 1:
        if split_msg[1] == 'chart':
            chart = build_chart(config, message.guild)
            await message.channel.send(f"```\n{chart}\n```")
        elif split_msg[1] == 'help':
            await message.author.send(help_str)
        else:
            logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
            await message.author.send(help_str)
    elif split_msg[0] == '!ac':
        await message.author.send(help_str)


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
        island_open = '✈️' if ac_data['users'][discord_user]['island'] else '⛔'
        fruit = fruit_lookup[ac_data['users'][discord_user]['fruit']]
        dodo_code = ac_data['users'][discord_user]['dodo_code']

        t_price = ac_data['users'][discord_user]['turnip_price']

        if ac_data['users'][discord_user]['turnip_time']:
            t_time = ac_data['users'][discord_user]['turnip_time'].strftime("%d/%m %H:%M PDT")
        else:
            t_time = ''

        out_table.append([discord_name, friend_code, dodo_code, island_open + fruit, t_price, t_time])

    return tabulate(out_table, headers=['User', 'Friend Code', 'Dodo', '🏝️  ', 'Turnip 🔔', 'Turnip ⏲️'], disable_numparse=True)
