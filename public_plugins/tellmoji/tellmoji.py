import logging
from discord import Embed, Color
from libs import tellmoji_libs

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <tellmoji.py> Tellmoji game, public plugin portion.")


async def action(**kwargs):
    """
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    split_message = message.content.split()

    if len(split_message) == 2:
        if split_message[0] == '!tellmoji':
            if len(message.mentions) > 0:
                target_member = message.mentions[0]
                challenge_embed = Embed(title="Tellmoji Challenge!", description=f"<@{target_member.id}>, click 👍 ️to accept, or 👎 to decline.", color=Color.green())
                challenge_message = await message.channel.send(f"<@{message.author.id}> has challenged <@{target_member.id}> to a Tellmoji match!", embed=challenge_embed)
                await challenge_message.add_reaction('👍')
                await challenge_message.add_reaction('👎')
