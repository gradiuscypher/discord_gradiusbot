import discord
import logging
import requests
from io import BytesIO
from discord import Embed, Color
from libs.infinity_management import mgmt_db
from libs.infinity_management import screenshot_processing

logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <infinity_user_pm.py> Infinity LTD commands for Pilot management in PM.")

pilot_manager = mgmt_db.PilotManager()

message_state = {}


async def action(**kwargs):
    """
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    split_message = message.content.split()

    if message.author.id in message_state.keys():
        if len(message.content) == 0:
            if message_state[message.author.id] == 'SEND_SCREENSHOT' and len(message.attachments) > 0:
                profile_image = BytesIO(requests.get(message.attachments[0].url).content)
                name_list = screenshot_processing.process_screenshot(profile_image)
                await confirm_names(name_list, message)
                message_state[message.author.id] = 'READY'

    elif len(split_message) == 2:
        if split_message[0] == '!pilot':
            if split_message[1] == 'screenshot':
                """
                when a user wants to provide a validation screenshot, required for a validated pilot account
                """
                await validate_screenshot(message)

            if split_message[1] == 'services':
                """
                interface for the services command: eg password for mumble etc
                """
                pass


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


async def confirm_names(name_list, message):
    await message.channel.send("The following messages will contain the detected character names...\n")

    for name in name_list:
        name_embed = Embed(title='Detected Character Name', description=f"{name}\nClick ✅ to confirm the character name.\nClick ✏️to edit the name.")
        embed_message = await message.channel.send(embed=name_embed)
        await embed_message.add_reaction("✅")
        await embed_message.add_reaction("✏")
