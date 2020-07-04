import asyncio
import datetime
from discord.enums import ChannelType
from discord import Embed, Color
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <user_cleanup.py> Provides tools for cleaning up inactive users.")


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

            if split_msg[1].isdigit():
                seen_members = set()
                after_date = datetime.datetime.now() - datetime.timedelta(int(split_msg[1]))
                text_channels = [c for c in guild.channels if c.type == ChannelType.text]

                for channel in text_channels:
                    current_channel_count += 1
                    async for target_message in channel.history(limit=None, after=after_date):
                        seen_members.add(target_message.author)

                    new_embed = Embed(title="User Cleanup Progress", color=Color.red())
                    new_embed.add_field(name="Scanned Channels", value=f"{current_channel_count}/{len(text_channels)}", inline=False)
                    new_embed.add_field(name="Active Members", value=f"{len(seen_members)}/{len(guild.members)}", inline=False)

                    if embed_status:
                        await embed_status.edit(embed=new_embed)
                    else:
                        new_message = await message.channel.send(embed=new_embed)
                        embed_status = new_message

                new_embed = Embed(title="User Cleanup Progress", color=Color.green())
                new_embed.add_field(name="Scanned Channels", value=f"{current_channel_count}/{len(text_channels)}", inline=False)
                new_embed.add_field(name="Active Members", value=f"{len(seen_members)}/{len(guild.members)}", inline=False)

                if embed_status:
                    await embed_status.edit(embed=new_embed)
                else:
                    await message.channel.send(embed=new_embed)

                unseen_members = list(set(guild.members) - seen_members)
                message_list = member_report(unseen_members)

                for alert in message_list:
                    await message.channel.send(alert)


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

        if (len(report_string) + len(new_line)) > 2000:
            message_list.append(f"```{report_string}```")
            report_string = new_line
        else:
            report_string += new_line

    if len(report_string) > 0:
        message_list.append(f"```{report_string}```")

    return message_list
