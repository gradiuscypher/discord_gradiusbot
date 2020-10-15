import asyncio
import logging
from public_plugins.trickcord_patches import trickcord_patches

logger = logging.getLogger('gradiusbot')

logger.info("[Message Event Plugin] <trickcord_patches.py>: Trickcord Edit Event patches.")

TRICKCORD_ID = 755580145078632508


async def action(**kwargs):
    event_type = kwargs['event_type']
    config = kwargs['config']
    spooked_role_id = config.getint('trickcord', 'spooked_role_id')

    if event_type == 'edit':
        before = kwargs['before']
        after = kwargs['after']

        # a trickortreater has left, so back to standby
        if len(after.embeds) > 0 and after.embeds[0].title == 'The trick-or-treater disappeared...':
            trickcord_patches.trickcord_state = 'STANDBY'

        # someone scare the trickortreater
        if len(after.embeds) > 0 and after.embeds[0].title == 'Oh no!':
            trickcord_patches.trickcord_state = 'STANDBY'

        # someone claimed the trickortreater, go to standby
        elif len(after.embeds) > 0 and after.embeds[0].title == 'Happy Halloween!':
            trickcord_patches.trickcord_state = 'STANDBY'
            await remove_spooked(after, spooked_role_id)

        elif after.author.id == 101103243991465984:
            if after.content == 'DEBUG-TRICK':
                print("DEBUGTRICK")
                trickcord_patches.trickcord_state = 'TRICK'

            elif after.content == 'DEBUG-TREAT':
                print("DEBUGTREAT")
                trickcord_patches.trickcord_state = 'TREAT'

            elif after.content == 'DEBUG-STANDBY':
                print("DEBUGSTANDBY")
                trickcord_patches.trickcord_state = 'STANDBY'

            elif after.content == 'UNSPOOK':
                print("UNSPOOK")
                await remove_spooked(after, spooked_role_id)


async def remove_spooked(message, spooked_role_id):
    guild = message.guild
    spooked_role = guild.get_role(spooked_role_id)
    spooked_users = spooked_role.members

    for member in spooked_users:
        await member.remove_roles(spooked_role)
