import json
import logging
from discord import Embed, Color
from datetime import datetime

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <image_collector.py> Collects images from specified channel on a server.")


async def action(**kwargs):
    """
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    split_message = message.content.split()
    admin_channel_id = config.getint('image_collector', 'admin_channel_id')
    guild = message.channel.guild

    if message.channel.id == admin_channel_id:
        if split_message[0] == '!ic':
            if len(split_message) == 3 and split_message[1] == 'collect':
                target_channel = guild.get_channel(int(split_message[2]))
                status_embed = Embed(title="Image Collection Script", color=Color.orange(), description="Starting image collection script...")

                message_count = 0
                file_count = 0
                if target_channel:
                    status_message = await message.channel.send(embed=status_embed)

                    async for msg in target_channel.history(limit=None):
                        message_count += 1

                        # collect message attachments
                        if len(msg.attachments) > 0:
                            attachment_count = 1
                            timestamp = msg.created_at
                            author = msg.author.id

                            for attachment in msg.attachments:
                                await attachment.save(f"images/{author}-{int(timestamp.timestamp())}-{attachment_count}")
                                file_count += 1
                                attachment_count += 1

                        if message_count % 50 == 0:
                            status_embed = Embed(title="Image Collection Script", color=Color.orange(),
                                                 description="Starting image collection script...")
                            status_embed.add_field(name="Messages processed", value=str(message_count))
                            status_embed.add_field(name="Files Saved", value=str(file_count))
                            await status_message.edit(embed=status_embed)

                    # Send final update
                    status_embed = Embed(title="Image Collection Script", color=Color.green(),
                                         description="Image collection script complete.")
                    status_embed.add_field(name="Messages processed", value=str(message_count))
                    status_embed.add_field(name="Files Saved", value=str(file_count))
                    await status_message.edit(embed=status_embed)

            elif split_message[1] == 'userjson':
                status_embed = Embed(title="Image Collection Script - User JSON", color=Color.green(),
                                     description="User JSON collection script complete.")
                member_dict = {}

                for member in guild.members:
                    member_dict[member.id] = {
                        'name': member.name,
                        'discriminator': member.discriminator,
                        'nick': member.nick,
                        'joined': member.joined_at.strftime('%Y-%m-%d %H:%M:%S')
                    }

                with open('users.json', 'w') as user_json:
                    user_json.write(json.dumps(member_dict))

                await message.channel.send(embed=status_embed)

