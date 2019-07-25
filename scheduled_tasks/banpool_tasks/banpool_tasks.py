import asyncio
import discord
import logging
import traceback
from discord import Embed, Color, Permissions
from concurrent.futures import CancelledError

from libs import banpool, banpool_configuration

banpool_manager = banpool.BanPoolManager()
banpool_config = banpool_configuration.BanpoolConfigManager()

# Setup Logging
logger = logging.getLogger('banpool_manager')
logger.setLevel(logging.DEBUG)

logger.info("[Scheduled Task] <banpool_tasks.py>: Scheduled tasks for the banpool.")


@asyncio.coroutine
async def action(client, config):
    admin_server_id = config.getint('banpool', 'admin_server_id')
    admin_chan_name = config.get('banpool', 'admin_chan')
    task_length = config.getint('banpool', 'task_length')
    mute_alerts = config.getbool('banpool', 'mute_alerts')
    admin_chan = None

    setting_up = True
    while setting_up:
        logger.info("Waiting for client to log in...")
        if client.is_ready():
            # Setup Admin Messaging
            admin_server = discord.utils.get(client.guilds, id=admin_server_id)
            admin_chan = discord.utils.get(admin_server.channels, name=admin_chan_name)
            setting_up = False
        await asyncio.sleep(5)

    while True:
        try:
            if client.is_ready():
                # Check each server for a user with a matching User ID and ban those found
                # Iterate through each server, looking for banned user IDs
                for guild in client.guilds:
                    # Build a list of all banned user IDs
                    banned_user_ids = []
                    all_banpool_list = banpool_manager.banpool_list()

                    # create a list of pools that the guild is subscribed to
                    banpool_list = [p for p in all_banpool_list if (banpool_config.is_guild_subscribed(guild.id, p.pool_name) or p.pool_name == 'global')]

                    # for each subscribed pool, get the user ids of banned users
                    for pool in banpool_list:
                        userlist = banpool_manager.banpool_user_list(pool.pool_name)

                        if userlist:
                            for user in userlist:
                                banned_user_ids.append(user.user_id)

                    # Validate bot's permissions
                    bot_perms = admin_chan.permissions_for(guild.me)

                    if not bot_perms.ban_members:
                        logger.error("The bot does not have ban permissions on {}[{}]".format(guild.name, guild.id))

                    else:
                        for user_id in banned_user_ids:
                            user = guild.get_member(user_id)

                            # If a user was found, check to see if there's an exception. If not, ban them.
                            if user and bot_perms.ban_members:
                                is_exception = banpool_manager.is_user_in_exceptions(user_id, guild.id)

                                if not is_exception:
                                    try:

                                        is_user_banned = banpool_manager.is_user_banned(user_id)
                                        user_bans = is_user_banned[0]
                                        pool_names = [p for p in user_bans.keys()]

                                        reason = user_bans[pool_names[0]].reason
                                        banpool_name = pool_names[0]
                                        banpool_manager.set_last_knowns(user_id, user.name, user.discriminator)

                                        # ban the user
                                        await guild.ban(user, reason="Banpool Bot [{}] - {}".format(banpool_name, reason))

                                        logger.debug('member is in the banpool and has no exceptions: {}'.format(user_id))
                                        ban_embed = Embed(title="User Banned via Task", color=Color.green())
                                        ban_embed.add_field(name="User Name", value=user.name + "#" + str(user.discriminator), inline=False)
                                        ban_embed.add_field(name="Server ID", value=guild.id, inline=True)
                                        ban_embed.add_field(name="User ID", value=user_id, inline=True)
                                        ban_embed.add_field(name="Banpool Name", value=banpool_name, inline=False)
                                        ban_embed.add_field(name="Ban Reason", value=reason, inline=False)
                                        ban_embed.set_footer(icon_url=guild.icon_url, text=guild.name)

                                        # send an ban announcement to the admin server
                                        if not mute_alerts:
                                            await admin_chan.send(embed=ban_embed)

                                        # check if the server has an announce channel set, if so, announce the ban
                                        announce_chan_id = banpool_config.get_announce_chan(guild.id)

                                        if announce_chan_id and not mute_alerts:
                                            announce_chan = discord.utils.get(guild.channels, id=announce_chan_id)
                                            announce_embed = Embed(title="User Banned via Task", color=Color.green())
                                            announce_embed.add_field(name="User Name", value=user.name + "#" + str(user.discriminator), inline=True)
                                            announce_embed.add_field(name="Nickname", value=user.nick, inline=True)
                                            announce_embed.add_field(name="User Profile", value=f"<@{user.id}>", inline=False)
                                            announce_embed.add_field(name="User ID", value=user_id, inline=False)
                                            announce_embed.set_footer(icon_url=guild.icon_url, text="See Admin Mains for more details")
                                            await announce_chan.send(embed=announce_embed)

                                    except:
                                        print("Failed to execute ban on {}[{}] server".format(guild.name, guild.id))
                                        print(traceback.format_exc())
                                        logger.error("Failed to execute ban on {}[{}] server".format(guild.name, guild.id))
                                        logger.error(traceback.format_exc())

            await asyncio.sleep(task_length)

        # ref: https://stackoverflow.com/questions/38652819/from-concurrent-futures-to-asyncio
        except CancelledError:
            raise NotImplementedError

        except RuntimeError:
            logger.error(traceback.format_exc())
            await asyncio.sleep(task_length)
            exit(0)

        except:
            logger.error(traceback.format_exc())
            await asyncio.sleep(task_length)
