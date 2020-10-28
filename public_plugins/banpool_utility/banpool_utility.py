from datetime import datetime, timedelta
import logging
from math import ceil
from typing import List, Any, Tuple
import discord
from discord import utils, Message
import traceback
from libs.banpool_configuration import BanpoolConfigManager


# Setup Logging

logger = logging.getLogger('gradiusbot')
logger.info("[Public Plugin] <banpool_utility.py>: This plugin provides utility functions for the banpool.")

# Setup the BanpoolConfiguration
bcm = BanpoolConfigManager()

help_string = """```
!bpu help : this command

!bpu recent-bans <MINUTES> : list user ids who have been kicked or banned within the last <MINUTES> minutes
```"""


def create_ascii_table(headers: List[str], columns: List[List[Any]],
                       column_sep: str = " | ", header_divider: str = "=") -> Tuple[str, List[str]]:
    # TODO: Get this into a package of its own, it's handy - Octo
    header: str = ""
    max_column_len: int = len(max(columns, key=len))
    content_lengths: List[int] = []
    rows: List[str] = []

    # Generate header
    for i, column in enumerate(columns):
        content_len = len(max([str(i) for i in column] + [headers[i]], key=len))
        content_lengths.append(content_len)
        header += headers[i].ljust(content_len) + column_sep
        column += [''] * (max_column_len - len(column))  # Pad each column to the length of the longest
    header = header[:-len(column_sep)]  # Cut the separator off the end
    header += "\n" + header_divider * ceil(len(header) / len(header_divider))  # Separate the header from the body

    # Generate rows
    for n in range(max_column_len):
        # Breaking down this awful, awful line:
        # For each column, extract the right data value, then left-justify it to the correct length for the column
        # Then combine all columns with the separator to finish the row
        rows.append(column_sep.join([str(x[n]).ljust(content_lengths[i]) for i, x in enumerate(columns)]))

    return header, rows


async def action(**kwargs):
    message: Message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    # Check to see if the message author is an administrator in the server or if they're part of the admin role
    is_admin_role = False
    guild_admin_role_id = bcm.get_admin_role_id(message.guild.id)

    split_content = message.content.split()

    if guild_admin_role_id:
        if utils.get(message.author.roles, id=guild_admin_role_id):
            is_admin_role = True

    if len(split_content) > 0 and split_content[0] == '!bpu':
        if message.channel.permissions_for(message.author).administrator or is_admin_role:
            if len(split_content) == 2:
                if split_content[1] == "help":
                    await message.channel.send(help_string)

            if len(split_content) == 3:
                if split_content[1] == "recent-bans":
                    # retrieve a list of bans made in the last x minutes
                    lookback = int(split_content[2])
                    logs_after = datetime.utcnow() - timedelta(minutes=lookback)

                    try:  # Try and get recent kicks and bans
                        entries: List[discord.AuditLogEntry] = await message.guild \
                            .audit_logs(action=discord.AuditLogAction.ban, after=logs_after).flatten()
                        entries += await message.guild \
                            .audit_logs(action=discord.AuditLogAction.kick, after=logs_after).flatten()
                    except discord.Forbidden:
                        message.channel.send(
                            "Permissions Error: Please grant the View Audit Log permission and try again")
                        return
                    except:
                        print(traceback.format_exc())
                        return

                    # Create table to post
                    target_names, target_ids, action_type, mod, timestamp = [], [], [], [], []
                    for entry in entries:
                        target_names.append(f"{entry.target.name}#{entry.target.discriminator}")
                        target_ids.append(entry.target.id)
                        action_type.append(entry.action.name)
                        mod.append(f"{entry.user.name}#{entry.user.discriminator}")
                        timestamp.append(int((datetime.utcnow() - entry.created_at).seconds / 60))

                    columns = [target_names, target_ids, action_type, mod, timestamp]
                    headers = ["user", "id", "action", "mod", "time (mins ago)"]
                    header, rows = create_ascii_table(headers, columns)

                    # Work out how many rows to a message we can fit in case of overflow
                    max_rows = int((1990 - len(header)) / (len(header) + 1))

                    # Paginate the table
                    for n in range(0, len(rows), max_rows):
                        message_text = "```md\n" + header
                        for row in rows[n:n + max_rows]:
                            message_text += "\n" + row
                        message_text += "\n```"
                        await message.channel.send(message_text)

                    # Paginate list of ids
                    for n in range(0, len(target_ids), 100):
                        message_text = "```" + ",".join([str(x) for x in target_ids[n:n + 100]]) + "```"
                        await message.channel.send(message_text)
