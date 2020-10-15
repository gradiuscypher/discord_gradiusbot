import logging
from discord import Embed, Color


logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <trickcord_patches.py> Patches to the Trickcord game for more fun.")

TRICKCORD_ID = 755580145078632508
trickcord_state = 'STANDBY'
trickcord_time = 0


async def action(**kwargs):
    """
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']
    global trickcord_state
    global trickcord_time

    spooked_role_id = config.getint('trickcord', 'spooked_role_id')
    allowed_delay = config.getint('trickcord', 'allowed_delay')
    spooked_role = message.guild.get_role(spooked_role_id)

    if message.author.id == TRICKCORD_ID:

        # a trickortreater has appeared, check what command is supposed to be said
        if len(message.embeds) > 0 and message.embeds[0].title == 'A trick-or-treater has stopped by!':
            if 'h!tricks' in message.embeds[0].description:
                trickcord_state = 'TRICK'
                trickcord_time = message.created_at

            if 'h!treats' in message.embeds[0].description:
                trickcord_state = 'TREAT'
                trickcord_time = message.created_at

    # if the author wasn't the trickortreater bot
    else:
        # debug tools
        if message.author.id == 101103243991465984 and message.content == 'showstate':
            await message.delete()
            await message.channel.send(trickcord_state)

        # add the author to the spooked role
        if trickcord_state == 'STANDBY':
            if message.content == 'h!trick' or message.content == 'h!treat':
                await message.author.add_roles(spooked_role, reason='User was spooked.')
                await message.channel.send("You sent the wrong command and were spooked by the trick-or-treater! 👻")

        elif trickcord_state == 'TRICK':
            if message.content == 'h!treat':
                await message.author.add_roles(spooked_role, reason='User was spooked.')
                await message.channel.send("You sent the wrong command and were spooked by the trick-or-treater! 👻")
            elif message.content == 'h!trick' and (message.created_at - trickcord_time)/1000 < allowed_delay:
                await message.author.add_roles(spooked_role, reason='User was spooked.')
                await message.channel.send("You replied too fast and were spooked by the trick-or-treater! 👻")

        elif trickcord_state == 'TREAT':
            if message.content == 'h!trick':
                await message.author.add_roles(spooked_role, reason='User was spooked.')
                await message.channel.send("You sent the wrong command and were spooked by the trick-or-treater! 👻")
            elif message.content == 'h!treat' and (message.created_at - trickcord_time)/1000 < allowed_delay:
                await message.author.add_roles(spooked_role, reason='User was spooked.')
                await message.channel.send("You replied too fast and were spooked by the trick-or-treater! 👻")

