# TODO: move all state changes into the function calls rather than in the chat commands
# TODO: after validation move character names to the DB

import discord
import logging
import re
import requests
import traceback
from io import BytesIO
from discord import Embed, Color
from libs.infinity_management import mgmt_db
from libs.infinity_management import screenshot_processing

logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <infinity_user_pm.py> Infinity LTD commands for Pilot management in PM.")

pilot_manager = mgmt_db.PilotManager()

message_state = {}
char_name_dict = {}
temp_name_bucket = {}

help_msg = """**Amos Bot - Command Help**\n
**Pilot Services**
```
validate - starts the screenshot validation process
```

**Other Commands**
```
help - this command
```
"""


async def action(**kwargs):
    """
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    split_message = message.content.split()

    # if the message author is in the state table, they may have already started a command, so check here first
    if message.author.id in message_state.keys():
        if len(split_message) == 0:
            if message_state[message.author.id] == 'SEND_SCREENSHOT' and len(message.attachments) > 0:
                profile_image = BytesIO(requests.get(message.attachments[0].url).content)
                name_list = screenshot_processing.process_screenshot(profile_image)
                await confirm_names(name_list, message)

        if len(split_message) == 1:
            if message_state[message.author.id] == 'VALIDATING' and split_message[0] == 'confirm':
                await message.channel.send("Thank you for confirming, your names and screenshot will be shared with the interview channel.")
                message_state[message.author.id] = 'READY'

            if message_state[message.author.id] == 'EDIT' and split_message[0] == 'confirm':
                await confirm_edit(message)

        if len(split_message) >= 3:
            if message_state[message.author.id] == 'VALIDATING' and split_message[0] == 'edit':
                await edit_names(message)

    elif len(split_message) == 1:
        if split_message[0] == 'validate':
            """
            when a user wants to provide a validation screenshot, required for a validated pilot account
            """
            await validate_screenshot(message)

        if split_message[0] == 'help':
            """
            when a user wants to provide a validation screenshot, required for a validated pilot account
            """
            await message.channel.send(help_msg)


async def validate_screenshot(message):
    message_state[message.author.id] = 'SEND_SCREENSHOT'
    await message.channel.send("Please provide a screenshot of the login screen showing the pilots on your account. Follow the guidelines below:\n```\n"
                               "- Include a screenshot *only*, do not upload a photo of your screen.\n"
                               "- Please insure that the character screen is horizontal and not vertical.\n"
                               "- Do not edit the screenshot in any way or you may prevent the software from capturing your character's names.\n"
                               "- Only include a screenshot of the game itself, if you're capturing from an emulator, do not capture the emulator window.\n"
                               "- Only include one screenshot each time you run the command. If you have alt accounts, run this command again.\n"
                               "- An example of an ideal screenshot can be found here: INCLUDE_LINK_HERE\n"
                               "- If you run into any issues, contact gradius#8902 on Discord.\n```")


async def confirm_edit(message):
    """
    Fires when a user is confirming the edit of a character name.
    :param message:
    :return:
    """
    name_bucket = temp_name_bucket[message.author.id]
    char_name_dict[message.author.id][name_bucket[0]] = name_bucket[1]
    character_names = char_name_dict[message.author.id]
    name_msg = ""

    for char_number in character_names.keys():
        name_msg += f"{char_number}) {character_names[char_number]}\n"

    await message.channel.send("Thank you for editing your character name. The current names are as follows:\n"
                               f"```\n{name_msg}\n```\n"
                               f"If you would like to edit another name, repeat the edit command like last time, otherwise type `confirm` to confirm your names.")

    message_state[message.author.id] = 'VALIDATING'


async def confirm_names(name_list, message):
    name_msg = ""
    namecount = 1
    char_name_dict[message.author.id] = {}

    for name in name_list:
        clean_name = re.sub('(\[|\().*(\]|\))', '', name).strip()
        char_name_dict[message.author.id][namecount] = clean_name
        name_msg += f"{namecount}) {clean_name}\n"
        namecount += 1

    await message.channel.send(f"These were the detected character names, please verify that they are correct.\n"
                               "If any of the names need to be corrected, use the edit command with the number associated with the name.\n"
                               "For example: `edit 1 MrCorrectName` would be the command to modify the first name to 'MrCorrectName'\n"
                               "Please be aware that both your screenshot and your provided names will be stored for future reference.\n\n"
                               f"```\n{name_msg}\n```\n"
                               f"If all listed names are correct please type `confirm`, otherwise please use the `edit` command.")

    message_state[message.author.id] = 'VALIDATING'


async def edit_names(message):
    # TODO: complete edit command
    split_message = message.content.split()

    try:
        target_number = int(split_message[1])
        correct_name = ' '.join(split_message[2:])
        old_name = char_name_dict[message.author.id][target_number]
        temp_name_bucket[message.author.id] = [target_number, correct_name]

        message_state[message.author.id] = 'EDIT'
        await message.channel.send(f"You would like to replace `{old_name}` with `{correct_name}`. If that is correct, please type `confirm` otherwise type `cancel`.")
    except:
        print(traceback.format_exc())
