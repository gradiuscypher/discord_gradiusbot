import asyncio
import logging
import traceback
from discord import Embed, Color, utils
from libs.banpool_configuration import BanpoolConfigManager
from libs.banpool import BanPoolManager

# Setup Logging
logger = logging.getLogger('banpool_configuration')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('banpool_configuration.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

logger.info("[Public Plugin] <banpool_configuration.py>: This plugin configures the banpool.")

bcm = BanpoolConfigManager()
bpm = BanPoolManager()

help_string = """
```
!bpc help : this command

!bpc banpool-list : list the available banpools to subscribe to

!bpc admin-role set <ROLE NAME>: set the admin role ID

!bpc admin-role get: get the admin role ID

!bpc configured-pools : list the banpools that are configured

!bpc set-announce-chan : set the channel to announce banpool changes in. Uses the channel the message was sent in.

!bpc send-test-message : send a test message to the configured announce-chan

!bpc subscribe <BANPOOL NAME> : subscribe to a banpool and add its bans to your server bans

!bpc unsubscribe <BANPOOL NAME> : unsubscribe from a banpool. you will no longer receive updated bans from this pool.
```
"""

# TODO: command to set admin role to allow others to control !bpc
# TODO: allow configured role to also execute !bpc


@asyncio.coroutine
async def action(**kwargs):
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    # Check to see if the message author is an administrator in the server or if they're part of the admin role
    is_admin_role = False
    guild_admin_role_id = bcm.get_admin_role_id(message.guild.id)

    if guild_admin_role_id:
        if utils.get(message.author.roles, id=guild_admin_role_id):
            is_admin_role = True

    if message.author.guild_permissions.administrator or is_admin_role:
        split_content = message.content.split()

        if len(split_content) > 0 and split_content[0] == '!bpc':
            if len(split_content) == 2:
                if split_content[1] == 'help':
                    await message.channel.send(help_string)

                if split_content[1] == 'banpool-list':
                    bp_list = bpm.banpool_list()

                    bp_embed = Embed(title="Available Ban Pools", color=Color.green())

                    for bp in bp_list:
                        bp_embed.add_field(name=bp.pool_name, value=bp.pool_description, inline=False)
                    await message.channel.send(embed=bp_embed)

                if split_content[1] == 'configured-pools':
                    # TODO: change display format of the banpools, dont need banlevel
                    pool_list = bcm.get_configured_pools(message.guild.id)
                    bp_embed = Embed(title="Configured BanPools", color=Color.green())

                    if pool_list:
                        for bp in pool_list:
                            bp_embed.add_field(name=bp.pool_name, value=bp.sub_level, inline=False)
                        await message.channel.send(embed=bp_embed)
                    else:
                        await message.channel.send("You don't have any banpool subscriptions. Use `!bpc help` for more help with the commands.")

                # User is setting the announcement channel
                if split_content[1] == 'set-announce-chan':
                    success = bcm.set_announce_chan(message.guild.id, message.channel.id,
                                                    message.author.name+'#'+message.author.discriminator,
                                                    message.author.id)

                    if success:
                        await message.channel.send('This channel will now be used for Banpool announcements.')

                    else:
                        await message.channel.send('Was unable to set announcement channel.')

                if split_content[1] == 'send-test-message':
                    announce_chan_id = bcm.get_announce_chan(message.guild.id)
                    target_channel = message.guild.get_channel(announce_chan_id)

                    if target_channel:
                        await target_channel.send('This is a test announcement message to the configured channel.')
                    else:
                        await message.channel.send('An announcement channel has not been set. Please set one with the `!bpc set-announce-chan` command in the desired channel.')

            if len(split_content) == 3:
                if split_content[1] == 'subscribe':
                    # add a banpool subscription with the level of 'ban' if the pool exists
                    pool_name = split_content[2]
                    success = bcm.set_pool_level(message.guild.id, pool_name, 'ban',
                                                 message.author.name+'#'+message.author.discriminator,
                                                 message.author.id)
                    if success:
                        await message.channel.send(f'Successfully subscribed the pool **{pool_name}**.')
                    else:
                        await message.channel.send(f'Unable to subscribe to the pool. Please validate that the pool name exists.')

                if split_content[1] == 'unsubscribe':
                    # remove the subscription if the pool exists and is subscribed to
                    pool_name = split_content[2]
                    success = bcm.unsubscribe(message.guild.id, pool_name)

                    if success:
                        await message.channel.send(f'Successfully unsubscribed from the pool **{pool_name}**.')
                    else:
                        await message.channel.send(f'Unable to unsubscribe from the pool. Please validate the pool name.')

                if split_content[1] == 'admin-role':
                    if split_content[2] == 'get':
                        # show the role name that's configured to use !bpc commands
                        admin_role_id = bcm.get_admin_role_id(message.guild.id)

                        if admin_role_id:
                            try:
                                # Try to find the role ID that is set as admin role
                                admin_role = utils.get(message.guild.roles, id=admin_role_id)

                                if admin_role:
                                    await message.channel.send(f'The role configured for admin is: `{admin_role.name}`')
                                else:
                                    await message.channel.send(f"The configured role ID `{admin_role_id}` does not exist on this server. Please set a new one")
                            except:
                                print(traceback.format_exc())
                        else:
                            await message.channel.send("There is no admin role configured. Set one with `!bpc admin-role set <ROLE NAME>`")

            if len(split_content) >= 4:
                if split_content[1] == 'admin-role':
                    if split_content[2] == 'set':
                        # set the role that will be able to run !bpc commands
                        admin_role_id = utils.get(message.guild.roles, name=' '.join(split_content[3:])).id

                        if admin_role_id:
                            success = bcm.set_admin_role_id(message.guild.id, admin_role_id, message.author.name+'#'+message.author.discriminator, message.author.id)

                            if success:
                                await message.channel.send('Admin role has been set.')
                            else:
                                await message.channel.send('Was unable to set admin role. A generic error has occurred, please contact gradius.')

                        else:
                            await message.channel.send('Unable to find role. Unable to set admin role.')

