import logging
from discord import Embed, Color

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
                if target_channel:
                    status_message = await message.channel.send(embed=status_embed)

                    async for msg in target_channel.history(limit=None):
                        message_count += 1

                        # collect message attachments
                        if len(msg.attachments) > 0:
                            for attachment in msg.attachments:
                                await message.channel.send(msg.author.id)
                                await message.channel.send(attachment.filename)

                        if message_count % 50 == 0:
                            status_embed = Embed(title="Image Collection Script", color=Color.orange(),
                                                 description="Starting image collection script...")
                            status_embed.add_field(name="Messages processed", value=str(message_count))
                            await status_message.edit(embed=status_embed)

                    # Send final update
                    status_embed = Embed(title="Image Collection Script", color=Color.green(),
                                         description="Image collection script complete.")
                    status_embed.add_field(name="Messages processed", value=str(message_count))
                    await status_message.edit(embed=status_embed)
