import logging
from discord import Embed, Color


logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <trickcord_patches.py> Patches to the Trickcord game for more fun.")

TRICKCORD_ID = 755580145078632508
trickcord_state = 'STANDBY'


async def action(**kwargs):
    """
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    spooked_role_id = config.getint('trickcord', 'spooked_role_id')
    spooked_role = message.guild.get_role(spooked_role_id)

    global trickcord_state

    if message.author.id == TRICKCORD_ID:

        # a trickortreater has appeared, check what command is supposed to be said
        if len(message.embeds) > 0 and message.embeds[0].title == 'A trick-or-treater has stopped by!':
            if 'h!tricks' in message.embeds[0].description:
                trickcord_state = 'TRICK'

            if 'h!treats' in message.embeds[0].description:
                trickcord_state = 'TREAT'

    # if the author wasn't the trickortreater bot
    else:
        # add the author to the spooked role
        if trickcord_state == 'STANDBY':
            if message.content == 'h!trick' or message.content == 'h!treat':
                await message.author.add_roles(spooked_role, reason='User was spooked.')
                await message.channel.send("You sent the wrong command and were spooked by the trick-or-treater! 👻")

        if trickcord_state == 'TRICK':
            if message.content == 'h!treat':
                await message.author.add_roles(spooked_role, reason='User was spooked.')
                await message.channel.send("You sent the wrong command and were spooked by the trick-or-treater! 👻")

        if trickcord_state == 'TREAT':
            if message.content == 'h!trick':
                await message.author.add_roles(spooked_role, reason='User was spooked.')
                await message.channel.send("You sent the wrong command and were spooked by the trick-or-treater! 👻")

        if message.author.id == 101103243991465984 and message.content == 'showstate':
            await message.delete()
            print(trickcord_state)
