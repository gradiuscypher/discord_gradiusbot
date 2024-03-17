# TODO: consider writing a cleanup schedule to clean up states after a period, to not take up resources

import datetime
import discord.utils
from discord.enums import ChannelType
from discord import Embed, Color
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <user_cleanup.py> Provides tools for cleaning up inactive users.")

# Stores state of the cleanup command to allow for editing and confirmation before executing
"""
state = {
    "<USER_ID>": {
        "state": "<STATE STRING>",
        "user_list": "<USERLIST>",
        "timestamp": "<LAST CHANGE DATETIME>"
        "remove_message": ""
    }
}
"""
state = {}
default_remove_msg = "You are being kicked from {} due to inactivity."


async def action(**kwargs):
    """
    :param kwargs:
    :return:
    """
    message = kwargs['message']
    config = kwargs['config']

    split_msg = message.content.split()
    sender_id = message.author.id
    guild = message.guild
    embed_status = None
    current_channel_count = 0

    if split_msg[0] == '!cleanup':

        if len(split_msg) == 2:

            # !cleanup <DIGIT>: check if digit, calculate inactivity via days since last message
            if split_msg[1].isdigit():
                seen_members = set()
                after_date = datetime.datetime.now() - datetime.timedelta(int(split_msg[1]))
                text_channels = [c for c in guild.channels if c.type == ChannelType.text]

                # iterate over every text channel, find all messages in split_msg[1] days, mark that user as active
                for channel in text_channels:
                    current_channel_count += 1
                    async for target_message in channel.history(limit=None, after=after_date):
                        seen_members.add(target_message.author)

                    # update the status embed with the current processing status
                    if embed_status:
                        await embed_status.edit(embed=build_embed(current_channel_count, len(text_channels), len(seen_members), len(guild.members), Color.red()))
                    else:
                        embed_status = await message.channel.send(embed=build_embed(current_channel_count, len(text_channels), len(seen_members), len(guild.members), Color.red()))

                # update the embed status with green to show that we're complete
                if embed_status:
                    await embed_status.edit(embed=build_embed(current_channel_count, len(text_channels), len(seen_members), len(guild.members), Color.green()))
                else:
                    await message.channel.send(embed=build_embed(current_channel_count, len(text_channels), len(seen_members), len(guild.members), Color.green()))

                # convert the unseen member list to a text report and send
                # TODO: note that you now need to review the list and confirm the clean up of members in the list
                unseen_members = list(set(guild.members) - seen_members)
                state[sender_id] = {'state': 'started', 'user_list': unseen_members,
                                    'timestamp': datetime.datetime.now()}

            # !cleanup list: list the current targets for cleanup
            if split_msg[1] == 'list' and sender_id in state.keys():
                message_list = member_report(state[sender_id]['user_list'])

                for message_entry in message_list:
                    await message.channel.send(message_entry)

            # !cleanup confirm: confirm that you are ready to kick the current list of inactive users
            if split_msg[1] == 'confirm' and sender_id in state.keys():
                cleanup_list = state[sender_id]['user_list']
                for user in cleanup_list:
                    # TODO: send message that was configured during setup
                    await user.send("")
                    await guild.kick(user, reason=f"User cleaned up via command run by {message.author.name}")

        elif len(split_msg) > 3:
            # !cleanup message: the message to send to users that are kicked
            if split_msg[1] == 'message' and sender_id in state.keys():
                state[sender_id]['remove_message'] = split_msg[2:]

            if split_msg[1] == 'remove' and sender_id in state.keys():
                # !cleanup remove <ROLE NAME> : remove anyone who's in this role from cleanup
                if split_msg[2] == 'role':
                    target_role = discord.utils.get(guild.roles, name=' '.join(split_msg[3:]))
                    if target_role:
                        remove_list = []
                        for target_member in state[sender_id]['user_list']:
                            if target_role.id in [r.id for r in target_member.roles]:
                                state[sender_id]['user_list'].remove(target_member)
                                remove_list.append(target_member)

                        await message.channel.send(f"**Removing these users from cleanup:**")
                        message_list = member_report(remove_list)
                        for message_entry in message_list[:-1]:
                            await message.channel.send(message_entry)

                # !cleanup remove userid <USER ID> : remove a specific user ID from cleanup
                if split_msg[2] == 'userid' and split_msg[3].isdigit():
                    target_member = discord.utils.get(guild.members, id=int(split_msg[3]))
                    if target_member in state[sender_id]['user_list']:
                        state[sender_id]['user_list'].remove(target_member)
                        await message.channel.send(f"<@{target_member.id}> was removed from the cleanup list.")


def member_report(member_list):
    """
    Returns a report string that properly formats a member list into a message
    :param member_list:
    :return:
    """
    message_list = []
    report_string = ""

    for member in member_list:
        new_line = f"{member.name}#{member.discriminator} - {[role.name for role in member.roles]}\n"

        if (len(report_string) + len(new_line)) >= 1990:
            message_list.append(f"```{report_string}```")
            report_string = new_line
        else:
            report_string += new_line

    if len(report_string) > 0:
        message_list.append(f"```{report_string}```")

    summary = f"\nThere are {len(member_list)} users scheduled to be removed from the server."
    message_list.append(summary)

    return message_list


def build_embed(current_channels, total_channels, current_members, total_members, color):
    new_embed = Embed(title="User Cleanup Progress", color=color)
    new_embed.add_field(name="Scanned Channels", value=f"{current_channels}/{total_channels}", inline=False)
    new_embed.add_field(name="Active Members", value=f"{current_members}/{total_members}", inline=False)

    return new_embed
