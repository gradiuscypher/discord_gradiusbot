# TODO: consider using JSON logging so that it's easier to dashboard errors
# TODO: integrate this workflow into when new players join the discord as well as re-validation of old players
# TODO: more scoped try/except blocks
# TODO: let the user know when a bug report was successful
# TODO: give users a step by step instruction with help.

import logging
import pathlib
import re
import requests
import traceback
from discord import Embed, Color, utils
from io import BytesIO
from libs.infinity_management import mgmt_db
from libs.infinity_management import screenshot_processing

logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <infinity_user_pm.py> Infinity LTD commands for Pilot management in PM.")

pilot_manager = mgmt_db.PilotManager()

message_state = {}
char_name_dict = {}
temp_name_bucket = {}
temp_delete_bucket = {}
temp_attachment_urls = {}

validate_screenshot_description = """Please provide a screenshot of the login screen showing the pilots on your account. Follow the guidelines below:

**Note**: The screenshots you share with the bot and the names contained in them will be saved for Infinity LTD records.

```
- Include a screenshot *only*, do not upload a photo of your screen.
- Please ensure that the character screen is horizontal and not vertical.
- Do not edit the screenshot in any way or you may prevent the bot from capturing your character's names.
- Only include a screenshot of the game itself, if you're capturing an emulator screen, do not capture the emulator window.
- Only include one screenshot each time you run the command. If you have alt accounts, run this command again.
- An example of an ideal screenshot can be found here: TODO:INCLUDE_LINK_HERE
- If you run into any issues, use the bug-report command or message anyone in the IT role on Discord.
```

**At any point in time, you can request for help regarding the step you're on by using the `help` command.**
"""

help_msg = """**Command Help**\n
This process is important because it allows us to automatically track our Pilot's character names and provide them with corp and alliance services.

**Your Current Progress**
">>>" - you are currently on this step
```
>>> 1) Start the validation process with the validate command
2) Send a screenshot of your Character Selection screen to this DM conversation
3) Edit any names that don't match your character names
4) Delete any names that the bot added that don't actually exist in your account. Please do not delete any valid characters, even if they aren't a part of the alliance.
5) Validate that all of the names are correct and send the confirm command to confirm your character names
```

Here are the currently available commands:
```
validate : starts the screenshot validation process
restart : restart the entire validation process, can be used at any time
remove-characters : this removes the characters from your account. Your account will be unverified until you add characters again.
list-characters : list the characters associated with your account.
bug-report <MESSAGE>: Allows you to send a message to the IT team if you have any issues. Please include the message in a single line and be as detailed as possible.
```
"""

validate_help_msg = """**Validation Help**\n

**Your Current Progress**
">>>" - you are currently on this step
```
1) Start the validation process with the validate command
2) Send a screenshot of your Character Selection screen to this DM conversation
3) Edit any names that don't match your character names
4) Delete any names that the bot added that don't actually exist in your account. Please do not delete any valid characters, even if they aren't a part of the alliance.
>>> 5) Validate that all of the names are correct and send the confirm command to confirm your character names
```

Here are the currently available commands:
```
help : this command
confirm : confirm the current character names listed
delete <CHARACTER_NUMBER> : delete the character before validation. Example: delete 1
edit <CHARACTER_NUMBER> <NEW_NAME> : edit the character name. Example: edit 1 Mr NewCharacter
list-characters : list the characters associated with your account.
restart : restart the validation process. use the validate command to start over.
bug-report <MESSAGE>: Allows you to send a message to the IT team if you have any issues. Please include the message in a single line and be as detailed as possible.
```
"""

edit_help_message = """**Edit Help**\n
You're currently editing a name. You can either confirm or cancel the edit.

**Your Current Progress**
">>>" - you are currently on this step
```
1) Start the validation process with the validate command
2) Send a screenshot of your Character Selection screen to this DM conversation
>>> 3) Edit any names that don't match your character names
4) Delete any names that the bot added that don't actually exist in your account. Please do not delete any valid characters, even if they aren't a part of the alliance.
5) Validate that all of the names are correct and send the confirm command to confirm your character names
```

Here are the currently available commands:
```
help : this command
confirm : confirm the current character name edit
cancel : cancel the current character name edit
list-characters : list the characters associated with your account.
restart : restart the validation process. use the validate command to start over.
bug-report <MESSAGE>: Allows you to send a message to the IT team if you have any issues. Please include the message in a single line and be as detailed as possible.
```
"""


delete_help_message = """**Deleting Help**\n

You're currently deleting a name. You can either confirm or cancel the delete.

**Please do not delete any character names that actually appear in the screen shot. If you do so, the screenshot will not be considered valid and will be subject to investigation.**
**Deleting valid character names prevents the bot from properly processing and tracking Pilots and their characters. Only delete names that we're found that don't actually exist.**

**Your Current Progress**
">>>" - you are currently on this step
```
1) Start the validation process with the validate command
2) Send a screenshot of your Character Selection screen to this DM conversation
3) Edit any names that don't match your character names
>>> 4) Delete any names that the bot added that don't actually exist in your account. Please do not delete any valid characters, even if they aren't a part of the alliance.
5) Validate that all of the names are correct and send the confirm command to confirm your character names
```

Here are the currently available commands:
```
help : this command
confirm : confirm the current character name delete
cancel : cancel the current character name delete
list-characters : list the characters associated with your account.
restart : restart the validation process. use the validate command to start over.
bug-report <MESSAGE>: Allows you to send a message to the IT team if you have any issues. Please include the message in a single line and be as detailed as possible.
```
"""


removing_help_message = """**Removing Help**\n
You're currently removing your character data. You can either confirm or cancel this action.

Here are the currently available commands:
```
help : this command
confirm : confirm the current character data removal
cancel : cancel the current character data removal
list-characters : list the characters associated with your account.
restart : restart the validation process. use the validate command to start over.
bug-report <MESSAGE>: Allows you to send a message to the IT team if you have any issues. Please include the message in a single line and be as detailed as possible.
```
"""


screenshot_help_message = """**Screenshot Validation Help**\n
You're currently validating a screenshot. You can either upload a screenshot of your character screen or run an available command.

**Your Current Progress**
">>>" - you are currently on this step
```
1) Start the validation process with the validate command
>>> 2) Send a screenshot of your Character Selection screen to this DM conversation
3) Edit any names that don't match your character names
4) Delete any names that the bot added that don't actually exist in your account. Please do not delete any valid characters, even if they aren't a part of the alliance.
5) Validate that all of the names are correct and send the confirm command to confirm your character names
```

Here are the currently available commands:
```
help : this command
cancel : cancel the screenshot upload process
restart : restart the entire validation process, can be used at any time
bug-report <MESSAGE>: Allows you to send a message to the IT team if you have any issues. Please include the message in a single line and be as detailed as possible.
```
"""


async def action(**kwargs):
    """
    [infinity]
    screenshot_dir =
    it_alert_chan_id =
    guild_id =
    validated_role_id =
    member_role_id =
    exception_alerts =
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    try:
        # grab the config values
        screenshot_dir = config.get('infinity', 'screenshot_dir')
        it_alert_chan_id = config.getint('infinity', 'it_alert_chan_id')
        guild_id = config.getint('infinity', 'guild_id')
        validated_role_id = config.getint('infinity', 'validated_role_id')
        member_role_id = config.getint('infinity', 'member_role_id')

        split_message = [s.lower() for s in message.content.split()]

        if message.author.id not in message_state.keys():
            message_state[message.author.id] = 'READY'

        # if the message author is in the state table, they may have already started a command, so check here first
        if message.author.id in message_state.keys():
            if len(split_message) == 0:
                if message_state[message.author.id] == 'SEND_SCREENSHOT' and len(message.attachments) > 0:
                    """
                    The user has sent a screenshot, and we're in the SEND_SCREENSHOT state
                    """
                    # TODO: move logic to helper function
                    try:
                        author_dir = f"{screenshot_dir}/{message.author.id}"
                        timestamp = message.created_at
                        attachment = message.attachments[0]
                        temp_attachment_urls[message.author.id] = attachment.url
                        attachment_content = requests.get(attachment.url).content
                        pathlib.Path(author_dir).mkdir(parents=True, exist_ok=True)
                        screenshot_name = f"{author_dir}/{int(timestamp.timestamp())}"

                        # save the screenshot to our pilots screenshot dir
                        with open(screenshot_name, 'wb') as screenshot_file:
                            screenshot_file.write(attachment_content)

                        # process the text in the screenshot and confirm names
                        profile_image = BytesIO(attachment_content)
                        name_list = screenshot_processing.process_screenshot(profile_image)
                        await confirm_names(name_list, message)

                    except:
                        logger.error("Failed to process screenshot", extra={'traceback': traceback.format_exc(),
                                                                            'sender_id': message.author.id})

                if message_state[message.author.id] == 'DEBUG':
                    await debug_test(message)

            if len(split_message) == 1:
                # if split_message[0] == 'crash-test':
                #     raise Exception

                if message_state[message.author.id] == 'DEBUG' and split_message[0] == 'exit':
                    await message.channel.send("Exiting debug mode.")
                    message_state[message.author.id] = 'READY'

                if split_message[0] == 'help':
                    """
                    user is requesting the help documentation
                    """
                    if message_state[message.author.id] == 'READY':
                        await message.channel.send(help_msg)
                    if message_state[message.author.id] == 'EDIT':
                        await message.channel.send(edit_help_message)
                    if message_state[message.author.id] == 'DELETING':
                        await message.channel.send(delete_help_message)
                    if message_state[message.author.id] == 'VALIDATING':
                        await message.channel.send(validate_help_msg)
                    if message_state[message.author.id] == 'SEND_SCREENSHOT':
                        await message.channel.send(screenshot_help_message)
                    if message_state[message.author.id] == 'REMOVING':
                        await message.channel.send(removing_help_message)

                # if split_message[0] == 'debug-test':
                #     """
                #     set the user in debug test mode
                #     """
                #     await debug_test(message)

                if split_message[0] == 'remove-characters':
                    """
                    user is requesting to delete stored characters
                    """
                    await remove_characters(message, config, client)

                if split_message[0] == 'list-characters':
                    """
                    user is requesting to list stored characters
                    """
                    await list_characters(message)

                if split_message[0] == 'restart':
                    """
                    Allows the user to restart the entire process.
                    """
                    message_state[message.author.id] = 'READY'
                    await message.channel.send("Restarting the user validation process.")

                if message_state[message.author.id] == 'READY' and split_message[0] == 'validate':
                    """
                    when a user wants to provide a validation screenshot, required for a validated pilot account
                    """
                    await validate_screenshot(message)

                if split_message[0] == 'confirm':
                    if message_state[message.author.id] == 'EDIT':
                        await confirm_edit(message, True)

                    elif message_state[message.author.id] == 'REMOVING':
                        await remove_characters(message, config, client)

                    elif message_state[message.author.id] == 'DELETING':
                        await delete_name(message)

                    elif message_state[message.author.id] == 'VALIDATING':
                        # TODO: move logic to helper function
                        author = message.author
                        character_names = [char_name_dict[author.id][char_number] for char_number in char_name_dict[author.id].keys()]
                        target_guild = client.get_guild(guild_id)
                        target_role = target_guild.get_role(validated_role_id)
                        target_member = target_guild.get_member(message.author.id)
                        member_role = target_guild.get_role(member_role_id)

                        try:
                            pilot_manager.add_pilot(author.id, author.name, author.discriminator, character_names=character_names)
                            logger.info(f"Creating a new Pilot <{author.id}, {author.name}, {author.discriminator}> [{character_names}]")
                            char_name_dict[author.id] = {}
                            message_state[message.author.id] = 'READY'
                        except:
                            logger.info(f"Error while creating a new Pilot <{author.id}>\n{traceback.format_exc()}")

                        await target_member.add_roles(target_role)
                        await message.channel.send("Thank you for validating your character names.")

                        # check to see if this user is part of a ticket channel and if so, message the channel with the screenshot and character names
                        # also, check to ensure they're not already a member to avoid spamming ticket channels when recuriters validate
                        if member_role not in target_member.roles:
                            for guild_channel in target_guild.channels:
                                if guild_channel.name.startswith('ticket-') and target_member in guild_channel.members:
                                    character_name_str = "\n".join(character_names)
                                    await guild_channel.send(f"{author.name} has completed their validation process. The character names are:\n```\n{character_name_str}\n```")
                                    await guild_channel.send(f"The validation screenshot sent in was: {temp_attachment_urls[author.id]}")

                if split_message[0] == 'cancel':
                    if message_state[message.author.id] == 'SEND_SCREENSHOT':
                        await message.channel.send("Canceling the screenshot upload process. Please restart this process with the `validate` command.")
                        message_state[message.author.id] = 'READY'

                    if message_state[message.author.id] == 'EDIT':
                        await confirm_edit(message, False)

                    if message_state[message.author.id] == 'REMOVING':
                        await remove_characters(message, config, client)

                    if message_state[message.author.id] == 'DELETING':
                        await delete_name(message)

            if len(split_message) == 2:
                if message_state[message.author.id] == 'VALIDATING' and split_message[0] == 'delete':
                    await delete_name(message)

            if len(split_message) >= 2:
                if split_message[0] == 'bug-report':
                    await bug_report(message, client, it_alert_chan_id)

            if len(split_message) >= 3:

                if message_state[message.author.id] == 'VALIDATING' and split_message[0] == 'edit':
                    await edit_names(message)
    except:
        it_alert_chan_id = config.getint('infinity', 'it_alert_chan_id')
        alert_chan = client.get_channel(it_alert_chan_id)
        exception_alerts = config.getboolean('infinity', 'exception_alerts')

        tb_str = traceback.format_exc()[:1950]
        tb_msg_str = f"```python\n{tb_str}\n```"
        logger.error("Uncaught exception", extra={'traceback': traceback.format_exc(),
                                                            'sender_id': message.author.id,
                                                            'discord_message': message.content,
                                                            'sender_name': f"{message.author.name}#{message.author.discriminator}"})

        if exception_alerts:
            await alert_message("Uncaught Exception", "", channel=alert_chan, color=Color.red(), details=tb_msg_str)


async def validate_screenshot(message):
    """
    Puts the user in the SEND_SCREENSHOT state which allows the user to upload their screenshot.
    :param message:
    :return:
    """
    message_state[message.author.id] = 'SEND_SCREENSHOT'
    await message.channel.send(validate_screenshot_description)


async def bug_report(message, client, it_alert_chan_id):
    split_message = message.content.split()

    report_content = ' '.join(split_message[1:])
    it_alert_chan = client.get_channel(it_alert_chan_id)
    fields = [
        {
            'name': "Reporter Name", 'value': f"{message.author.name}#{message.author.discriminator}"
        },
        {
            'name': "Reporter", 'value': f"<@{message.author.id}>"
        }
    ]
    await alert_message("User Report", report_content, channel=it_alert_chan, fields=fields, color=Color.orange())


async def confirm_edit(message, confirm):
    """
    Fires when a user is confirming the edit of a character name.
    :param message:
    :param confirm:
    :return:
    """
    try:
        if confirm:
            name_bucket = temp_name_bucket[message.author.id]
            logger.info(f"Replacing <{message.author.id}> {char_name_dict[message.author.id][name_bucket[0]]} with {name_bucket[1]}")
            char_name_dict[message.author.id][name_bucket[0]] = name_bucket[1]
            character_names = char_name_dict[message.author.id]
            name_msg = ""

            for char_number in character_names.keys():
                name_msg += f"{char_number}) {character_names[char_number]}\n"

            await message.channel.send("Thank you for editing your character name. The current names are as follows:\n"
                                       f"```\n{name_msg}\n```\n"
                                       f"If you would like to edit another name, repeat the edit command like last time, otherwise type `confirm` to confirm your names.")

            message_state[message.author.id] = 'VALIDATING'

        else:
            character_names = char_name_dict[message.author.id]
            name_msg = ""

            for char_number in character_names.keys():
                name_msg += f"{char_number}) {character_names[char_number]}\n"

            await message.channel.send(f"Canceling the name edit command. Your current names are as follows:\n"
                                       f"```\n{name_msg}\n```\n"
                                       f"If you would like to edit another name, repeat the edit command like last time, otherwise type `confirm` to confirm your names.")
            message_state[message.author.id] = 'VALIDATING'
    except:
        logger.error("Uncaught exception", extra={'traceback': traceback.format_exc(),
                                                  'sender_id': message.author.id,
                                                  'discord_message': message.content,
                                                  'sender_name': f"{message.author.name}#{message.author.discriminator}"})


async def confirm_names(name_list, message):
    """
    Starts the name confirmation process once the screenshots have been detected.
    :param name_list:
    :param message:
    :return:
    """
    name_msg = ""
    namecount = 1
    char_name_dict[message.author.id] = {}

    for name in name_list:
        clean_name = re.sub('(\[|\().*(\]|\))', '', name).strip()
        char_name_dict[message.author.id][namecount] = clean_name
        name_msg += f"{namecount}) {clean_name}\n"
        namecount += 1

    await message.channel.send(f"These were the detected character names, please verify that they are correct.\n\n"
                               "If any of the names need to be corrected, use the edit command with the number associated with the name.\n"
                               "For example: `edit 1 MrCorrectName` would be the command to modify the first name to 'MrCorrectName'\n\n"
                               "If you would like to remove a character from the list, use the `delete` command.\n"
                               "For example: `delete 2` would delete the second character from the list before submitting.\n\n"
                               "Please be aware that both your screenshot and your provided names will be stored for future reference.\n\n"
                               f"```\n{name_msg}\n```\n"
                               f"If all listed names are correct please type `confirm`, otherwise please use the `edit` command.")

    message_state[message.author.id] = 'VALIDATING'


async def debug_test(message):
    """
    A debug method that shows what text is being detected in images
    :return:
    """
    if message_state[message.author.id] == 'DEBUG':
        profile_image = BytesIO(requests.get(message.attachments[0].url).content)
        text_list = screenshot_processing.process_screenshot(profile_image, debug=True)
        await message.channel.send(f"{text_list}")

    elif message_state[message.author.id] == 'READY':
        await message.channel.send("Send your debug image now to see what is detected.")
        message_state[message.author.id] = 'DEBUG'


async def delete_name(message):
    """
    Allows the player to delete a name from the list before submitting, in the case of a bugged text detection.
    :param message:
    :return:
    """
    if message_state[message.author.id] == 'VALIDATING':
        if len(char_name_dict[message.author.id]) > 1:
            target_character_number = int(message.content.split()[1])
            temp_delete_bucket[message.author.id] = target_character_number
            await message.channel.send(f"You've chosen to delete the character named {char_name_dict[message.author.id][target_character_number]}. To confirm, type `confirm`, otherwise type `cancel` to return to the validation process without deleting.")
            message_state[message.author.id] = 'DELETING'
        else:
            await message.channel.send(f"You can only delete a character if you have more than one character detected.")

    elif message_state[message.author.id] == 'DELETING' and message.content == 'confirm':
        target_character_number = temp_delete_bucket[message.author.id]
        del char_name_dict[message.author.id][target_character_number]
        await message.channel.send("That character name has been deleted.")
        message_state[message.author.id] = 'VALIDATING'

    elif message_state[message.author.id] == 'DELETING' and message.content == 'cancel':
        await message.channel.send("Canceling the request to delete the character.")
        message_state[message.author.id] = 'VALIDATING'


async def remove_characters(message, config, client):
    """
    The user wants to restart the character name adding process by removing their characters.
    Preventing someone from removing individual characters limits people trying to hid alt names
    :param message:
    :param config:
    :param client:
    :return:
    """
    if message_state[message.author.id] == 'REMOVING':
        if message.content == 'cancel':
            await message.channel.send("Canceling the request to remove your characters.")
            message_state[message.author.id] = 'READY'

        else:
            await message.channel.send("Removing your character names. Please use the `validate` command to add another screenshot like before.")
            message_state[message.author.id] = 'READY'
            target_pilot = pilot_manager.get_pilot(message.author.id)
            target_pilot.remove_characters()

            guild_id = config.getint('infinity', 'guild_id')
            validated_role_id = config.getint('infinity', 'validated_role_id')
            target_guild = client.get_guild(guild_id)
            target_role = target_guild.get_role(validated_role_id)
            target_member = target_guild.get_member(message.author.id)
            await target_member.remove_roles(target_role, reason="[Amos BOT] - The user has removed their validated character names.")
            logger.info("Removing all characters", extra={'sender_id': message.author.id,
                                                          'discord_message': message.content,
                                                          'sender_name': f"{message.author.name}#{message.author.discriminator}"})

    elif message_state[message.author.id] == 'READY':
        await message.channel.send("This will allow you to remove your current character names and start over with the screenshot validation. "
                                   "This is useful if you delete a character and no longer want it tracked. "
                                   "Until you add your characters back, you will be unable to use any Pilot services that require character names. "
                                   "If you want to remove your characters now, type `confirm`, otherwise type `cancel`")
        message_state[message.author.id] = 'REMOVING'


async def edit_names(message):
    """
    Starts the name editing process for a provided name
    :param message:
    :return:
    """
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


async def list_characters(message):
    """
    Lists the Pilots characters.
    :param message:
    :return:
    """
    target_pilot = pilot_manager.get_pilot(message.author.id)

    if target_pilot:
        character_list = [character.name for character in target_pilot.characters]
    else:
        character_list = []

    if message.author.id in char_name_dict.keys():
        unconfirmed_names = [char_name_dict[message.author.id][char_number] for char_number in char_name_dict[message.author.id].keys()]
        unconfirmed_string = '\n'.join(unconfirmed_names)
    else:
        unconfirmed_string = ''

    if len(character_list) > 0:
        character_string = '\n'.join(character_list)
        await message.channel.send(f"**Characters associated with this account:**\n```\n{character_string}```\n\n"
                                   f"**Unconfirmed character names:**\n```\n{unconfirmed_string}\n```")
    else:
        await message.channel.send("There are no characters associated with this account.\n\n"
                                   f"**Unconfirmed character names:**\n```\n{unconfirmed_string}\n```")


async def alert_message(title, message, channel, fields=None, color=Color.darker_grey(), details=None):
    if not channel:
        pass

    report_embed = Embed(title=title, color=color, description=message)

    if fields:
        for field in fields:
            report_embed.add_field(name=field['name'], value=field['value'], inline=True)

    await channel.send(embed=report_embed)

    if details:
        await channel.send(details)
