import asyncio
import logging
import traceback
from libs.ac_libs import AcManager, help_str
from pytz import all_timezones

logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <animal_crossing.py> Provides tools for the game Animal Crossing.")


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

    if split_msg[0] == '!ac' and len(split_msg) == 1:
        await message.channel.send(help_str)

    elif split_msg[0] == '!ac' and len(split_msg) > 1:

        if split_msg[1] == 'turnip':
            if split_msg[2] == 'add' and len(split_msg) == 4:
                try:
                    target_user = ac_manager.user_exists(sender_id)

                    if target_user and target_user.time_zone != '':
                        turnip_price = int(split_msg[3])
                        success = add_turnip(sender_id, turnip_price)

                        if success:
                            await message.add_reaction("🆗")
                        else:
                            await message.add_reaction("❌")
                            logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
                    else:
                        await message.add_reaction("❌")
                        await message.channel.send("Before adding Turnip prices, please set your time zone. Use `!ac timezone help` to get started.")

                except:
                    await message.add_reaction("❌")
                    logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
                    logger.error(traceback.format_exc())

        elif split_msg[1] == 'friendcode' and len(split_msg) == 3:
            friendcode = split_msg[2]

            try:
                success = set_friendcode(sender_id, friendcode)

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
                success = set_fruit(sender_id, target_fruit)

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
                    success = set_island(sender_id, True)
                if len(split_msg) == 4:
                    dodo_code = split_msg[3]
                    success = set_island(sender_id, True, dodo_code=dodo_code)

            elif split_msg[2] == 'close':
                if len(split_msg) == 3:
                    success = set_island(sender_id, False, dodo_code='')

            if success:
                await message.add_reaction("🆗")
            else:
                await message.add_reaction("❌")
                logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")

        elif split_msg[1] == 'timezone':
            if split_msg[2] == 'help':
                await message.channel.send("Set your time zone for more accurate tracking. The list of time zones can be found here: https://gist.github.com/gradiuscypher/92905b1cc24dea2b17cc1e8959d18999")
                await message.channel.send("\nPlease copy/paste the time zone exactly as you find it on the list.")
                await message.channel.send("\nExample Command: `!ac timezone set America/Los_Angeles`")

            elif split_msg[2] == 'set' and len(split_msg) >= 4:
                timezone_str = split_msg[3]

                if timezone_str in all_timezones:
                    success = set_timezone(sender_id, timezone_str)

                    if success:
                        await message.add_reaction("🆗")
                    else:
                        await message.add_reaction("❌")
                        logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")
                else:
                    await message.add_reaction("❌")
                    await message.channel.send(
                        "Not a valid time zone. Refer to the link in the `!ac timezone help` command for the list of time zones.")
                    logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")

        elif split_msg[1] == 'help':
            await message.channel.send(help_str)

        else:
            await message.channel.send("You did not provide a properly formatted command. Check out !ac help for more info.")
            logger.debug(f"FAILED COMMAND - {message.author.id} : {message.content}")


def add_turnip(discord_id, turnip_price):
    """
    Adds the most current turnip price to the users data and saves the old value to historical data
    :param discord_id:
    :param turnip_price:
    :param server_id:
    :return:
    """
    try:
        # check if the user exists, if they don't create them
        # add the new price to the users data
        # return true
        target_user = ac_manager.user_exists(discord_id)

        if target_user:
            # the user does exist
            target_user.add_price(turnip_price)
        else:
            new_user = ac_manager.add_user(discord_id)
            new_user.add_price(turnip_price)

        return True

    except:
        logger.error(traceback.format_exc())
        return False


def set_friendcode(discord_id, friendcode):
    """
    Sets the friendcode for the discord ID
    :param discord_id:
    :param friendcode:
    :return:
    """
    try:
        target_user = ac_manager.user_exists(discord_id)

        if target_user:
            target_user.update_friend_code(friendcode)
        else:
            new_user = ac_manager.add_user(discord_id)
            new_user.update_friend_code(friendcode)

        return True

    except:
        logger.error(traceback.format_exc())
        return False


def set_fruit(discord_id, fruit):
    """
    Sets the fruit for the discord ID
    :param discord_id:
    :param fruit:
    :return:
    """
    try:
        target_user = ac_manager.user_exists(discord_id)

        if target_user:
            target_user.update_fruit(fruit)
        else:
            new_user = ac_manager.add_user(discord_id)
            new_user.update_fruit(fruit)

        return True

    except:
        logger.error(traceback.format_exc())
        return False


def set_island(discord_id, island_open, dodo_code=''):
    """
    Sets the boolean whether the Island is open or not.
    :param discord_id:
    :param island_open:
    :param dodo_code:
    :return:
    """
    try:
        target_user = ac_manager.user_exists(discord_id)

        if target_user:
            target_user.update_island(island_open, dodo_code)
        else:
            new_user = ac_manager.add_user(discord_id)
            new_user.update_island(island_open, dodo_code)

        return True

    except:
        logger.error(traceback.format_exc())
        return False


def set_timezone(discord_id, timezone_str):
    """
    Set the user's timezone string
    :param discord_id:
    :param timezone_str:
    :return:
    """
    try:
        target_user = ac_manager.user_exists(discord_id)

        if target_user:
            target_user.update_timezone(timezone_str)
        else:
            new_user = ac_manager.add_user(discord_id)
            new_user.update_timezone(timezone_str)

        return True

    except:
        logger.error(traceback.format_exc())
        return False
