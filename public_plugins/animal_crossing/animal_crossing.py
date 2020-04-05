import asyncio
import logging
import pytz
from tabulate import tabulate
from libs.ac_libs import AcManager, help_str

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <animal_crossing.py> Provides tools for the game Animal Crossing.")

DISPLAY_CHAR_LIMIT = 32
ac_manager = AcManager()


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
        if split_msg[1] == 'stonks':
            user_list = ac_manager.user_list()
            chart = turnip_chart(user_list, message.guild)
            await message.channel.send(f"**Turnip Prices**\n```\n{chart}\n```")

        elif split_msg[1] == 'travel':
            user_list = ac_manager.user_list()
            chart = travel_chart(user_list, message.guild)
            await message.channel.send(f"**Travel List**\n```\n{chart}\n```")

        elif split_msg[1] == 'social':
            user_list = ac_manager.user_list()
            chart = social_chart(user_list, message.guild)
            await message.channel.send(f"**Social List**\n```\n{chart}\n```")

        elif split_msg[1] == 'help':
            await message.author.send(help_str)

        else:
            logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
            await message.author.send(help_str)

    elif split_msg[0] == '!ac':
        await message.author.send(help_str)


def turnip_chart(user_list, guild):
    """
    Builds the chart for displaying turnip prices
    :param user_list:
    :param guild:
    :return:
    """
    out_table = []

    for user in user_list:
        discord_user = guild.get_member(user.discord_id)
        if discord_user:
            discord_name = clean_string(discord_user.display_name, max_length=DISPLAY_CHAR_LIMIT)
        else:
            discord_name = user.discord_id
        last_price = user.turnip_prices[-1] if len(user.turnip_prices) > 0 else None

        if last_price:
            t_price = user.turnip_prices[-1].price
            t_time = user.turnip_prices[-1].time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(user.time_zone))
            tz_formatted = t_time.strftime("%d/%m %H:%M ") + user.time_zone
        else:
            t_price = ""
            tz_formatted = ""

        out_table.append([discord_name, t_price, tz_formatted])

    return tabulate(out_table, headers=['User', 'Turnip 🔔', 'Turnip ⏲️'], disable_numparse=True)


def social_chart(user_list, guild):
    """
    Builds the chart to display social data for Animal Crossing
    :param user_list:
    :param guild:
    :return:
    """
    out_table = []

    for user in user_list:
        discord_user = guild.get_member(user.discord_id)
        if discord_user:
            discord_name = clean_string(discord_user.display_name, max_length=DISPLAY_CHAR_LIMIT)
        else:
            discord_name = user.discord_id

        friend_code = clean_string(user.friend_code, max_length=18)
        out_table.append([discord_name, friend_code])

    return tabulate(out_table, headers=['User', 'Friend Code'], disable_numparse=True)


def travel_chart(user_list, guild):
    """
    Builds the chart to display travel data for Animal Crossing
    :param user_list:
    :param guild:
    :return:
    """
    out_table = []
    fruit_lookup = {'apple': '🍎', 'pear': '🍐', 'cherry': '🍒', 'peach': '🍑', 'orange': '🍊'}

    for user in user_list:
        discord_user = guild.get_member(user.discord_id)
        if discord_user:
            discord_name = clean_string(discord_user.display_name, max_length=DISPLAY_CHAR_LIMIT)
        else:
            discord_name = user.discord_id

        island_open = '✈️' if user.island_open else '⛔'
        fruit = fruit_lookup[user.fruit] if user.fruit != '' else ''
        dodo_code = clean_string(user.dodo_code, max_length=8)
        out_table.append([discord_name, dodo_code, island_open + fruit])

    return tabulate(out_table, headers=['User', 'Dodo', '🏝️  '], disable_numparse=True)


def clean_string(input_string, max_length=0):
    """
    Removes bad characters from the string known to cause formatting issues.
    :return:
    """
    bad_chars = "`@"
    for bad_char in bad_chars:
        input_string = input_string.replace(bad_char, "")

    if max_length > 0:
        return input_string[:max_length]
    else:
        return input_string
