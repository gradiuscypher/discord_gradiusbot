import asyncio
import discord
import logging
import traceback
from discord import Embed, Color

from libs import banpool, banpool_configuration

banpool_manager = banpool.BanPoolManager()
banpool_config = banpool_configuration.BanpoolConfigManager()

# Setup Logging
logger = logging.getLogger('banpool_manager')
logger.setLevel(logging.DEBUG)

logger.info("[Event Plugin] <banpool_events.py>: This plugin manages banpool related events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']
    config = kwargs['config']
    client = kwargs['client']

    if event_type == 'member.unban':
        # Grab configuration values
        admin_server_id = config.getint('banpool', 'admin_server_id')
        admin_chan_name = config.get('banpool', 'admin_chan')
        admin_server = discord.utils.get(client.guilds, id=admin_server_id)
        admin_chan = discord.utils.get(admin_server.channels, name=admin_chan_name)

        user = kwargs['user']
        guild = kwargs['guild']

        try:
            result = banpool_manager.is_user_banned(user.id)

            # User is in banpool, so we need to add an exception
            if result[1]:
                logger.debug("member_unban event was caught for banpool ID: {}".format(user.id))
                banpool_manager.add_user_to_exceptions(user.id, guild.id)

                unban_embed = Embed(title="User Exception Added", color=Color.orange())
                unban_embed.add_field(name="User Name", value=user.name + "#" + str(user.discriminator), inline=False)
                unban_embed.add_field(name="Server ID", value=guild.id, inline=True)
                unban_embed.add_field(name="User ID", value=user.id, inline=True)
                unban_embed.set_footer(icon_url=guild.icon_url, text=guild.name)

                await admin_chan.send(embed=unban_embed)

                # check if the server has an announce channel set, if so, announce the ban
                announce_chan_id = banpool_config.get_announce_chan(guild.id)

                if announce_chan_id:
                    announce_chan = discord.utils.get(guild.channels, id=announce_chan_id)
                    announce_embed = Embed(title="User Exception Added", color=Color.orange())
                    announce_embed.add_field(name="User Name", value=user.name + "#" + str(user.discriminator), inline=True)
                    announce_embed.add_field(name="User Profile", value=f"<@{user.id}>", inline=False)
                    announce_embed.add_field(name="User ID", value=user.id, inline=False)
                    await announce_chan.send(embed=announce_embed)
        except:
            logger.error(traceback.format_exc())

    if event_type == 'member.join':
        # Grab configuration values
        admin_server_id = config.getint('banpool', 'admin_server_id')
        admin_chan_name = config.get('banpool', 'admin_chan')

        admin_server = discord.utils.get(client.guilds, id=admin_server_id)
        admin_chan = discord.utils.get(admin_server.channels, name=admin_chan_name)
        member = kwargs['member']
        guild = member.guild

        try:
            result = banpool_manager.is_user_banned(member.id)

            # The member is banpooled and we might need to ban them
            if result[1]:
                # check if the guild is subscribed to any banpool the user is in
                banpool_list = [p for p in result[0]]

                is_subscribed = False
                for pool in banpool_list:
                    check_subscription = banpool_config.is_guild_subscribed(guild.id, pool)

                    if check_subscription:
                        is_subscribed = True
                        target_pool = pool

                if is_subscribed:
                    banpool_name = target_pool
                    reason = result[0][target_pool].reason
                    logger.debug('member_join was caught for banpool ID: {}'.format(member.id))
                    user_id = member.id
                    user_name = member.name
                    user_discriminator = member.discriminator
                    server_id = member.guild.id

                    is_exception = banpool_manager.is_user_in_exceptions(user_id, server_id)

                    bot_perms = admin_chan.permissions_for(member.guild.me)

                    if not is_exception and bot_perms.ban_members:
                        logger.debug('member joined is in the banpool and has no exceptions: {}'.format(member.id))
                        banpool_manager.set_last_knowns(user_id, user_name, user_discriminator)

                        ban_embed = Embed(title="User Banned on Join", color=Color.green())
                        ban_embed.add_field(name="User Name", value=user_name + "#" + str(user_discriminator), inline=False)
                        ban_embed.add_field(name="Server ID", value=guild.id, inline=True)
                        ban_embed.add_field(name="User ID", value=user_id, inline=True)
                        ban_embed.add_field(name="Banpool Name", value=banpool_name, inline=False)
                        ban_embed.add_field(name="Ban Reason", value=reason, inline=False)
                        ban_embed.set_footer(icon_url=guild.icon_url, text=guild.name)
                        await admin_chan.send(embed=ban_embed)

                        # check if the server has an announce channel set, if so, announce the ban
                        announce_chan_id = banpool_config.get_announce_chan(guild.id)

                        if announce_chan_id:
                            announce_chan = discord.utils.get(guild.channels, id=announce_chan_id)
                            announce_embed = Embed(title="User Banned on Join", color=Color.green())
                            announce_embed.add_field(name="User Name", value=member.name + "#" + str(member.discriminator), inline=True)
                            announce_embed.add_field(name="Nickname", value=member.nick, inline=True)
                            announce_embed.add_field(name="User Profile", value=f"<@{member.id}>", inline=False)
                            announce_embed.add_field(name="User ID", value=user_id, inline=False)
                            announce_embed.set_footer(icon_url=guild.icon_url, text="See Admin Mains for more details")
                            await announce_chan.send(embed=announce_embed)

                        await guild.ban(member, reason="Banpool Bot [{}] - {}".format(banpool_name, reason))
        except:
            logger.error(traceback.format_exc())

