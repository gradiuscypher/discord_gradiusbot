import asyncio
import discord
import logging
import traceback
from libs import banpool
from discord import Embed, Color

banpool_manager = banpool.BanPoolManager()

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
                unban_embed.add_field(name="Server ID", value=guild.id, inline=True)
                unban_embed.add_field(name="User ID", value=user.id, inline=True)
                unban_embed.add_field(name="User Name", value=user.name + "#" + str(user.discriminator), inline=True)
                unban_embed.set_thumbnail(url=user.avatar_url)
                unban_embed.set_footer(icon_url=guild.icon_url, text=guild.name)

                await admin_chan.send(embed=unban_embed)
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

            # The member is banpooled and we need to ban them
            if result[1]:
                banpool_name = result[0]
                reason = result[2]
                logger.debug('member_join was caught for banpool ID: {}'.format(member.id))
                user_id = member.id
                user_name = member.name
                user_discriminator = member.discriminator
                user_avatar_url = member.avatar_url
                server_id = member.guild.id
                server_icon_url = member.guild.icon_url
                server_name = member.guild.name

                is_exception = banpool_manager.is_user_in_exceptions(user_id, server_id)

                bot_perms = admin_chan.permissions_for(member.guild.me)

                if not is_exception and bot_perms.ban_members:
                    logger.debug('member joined is in the banpool and has no exceptions: {}'.format(member.id))
                    ban_embed = Embed(title="User Banned on Join", color=Color.green())
                    ban_embed.add_field(name="Server ID", value=server_id, inline=True)
                    ban_embed.add_field(name="User ID", value=user_id, inline=True)
                    ban_embed.add_field(name="User Name", value=user_name + "#" + str(user_discriminator), inline=False)
                    ban_embed.add_field(name="Ban Reason", value=reason, inline=False)
                    ban_embed.set_thumbnail(url=user_avatar_url)
                    ban_embed.set_footer(icon_url=server_icon_url, text=server_name)

                    await guild.ban(member, reason="Banpool Bot [{}] - {}".format(banpool_name, reason))
                    await admin_chan.send(embed=ban_embed)
        except:
            logger.error(traceback.format_exc())

