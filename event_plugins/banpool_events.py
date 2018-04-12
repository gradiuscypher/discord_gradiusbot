import asyncio
import discord
import logging
import traceback
from libs import banpool
from discord import Embed, Color

print("[Event Plugin] <banpool_events.py>: This plugin manages banpool related events.")

banpool_manager = banpool.BanPoolManager()

# Setup Logging
logger = logging.getLogger('banpool_manager')
logger.setLevel(logging.DEBUG)


# NOTE: In this case object_after is the server
@asyncio.coroutine
async def action(member, client, config, event_type, object_after=None):
    admin_server_id = config.get('banpool', 'admin_server_id')
    admin_chan_name = config.get('banpool', 'admin_chan')
    admin_server = discord.utils.get(client.servers, id=admin_server_id)
    admin_chan = discord.utils.get(admin_server.channels, name=admin_chan_name)

    # Someone was unbanned, check to see if they're in the banpool, if so, add an exception for this server
    if event_type == "member_unban":
        try:
            result = banpool_manager.is_user_banned(member.id)

            # User is in banpool, so we need to add an exception
            if result[1]:
                logger.debug("member_unban event was caught for banpool ID: {}".format(member.id))
                banpool_manager.add_user_to_exceptions(member.id, object_after.id)

                unban_embed = Embed(title="User Exception Added", color=Color.orange())
                unban_embed.add_field(name="Server ID", value=object_after.id, inline=True)
                unban_embed.add_field(name="User ID", value=member.id, inline=True)
                unban_embed.add_field(name="User Name", value=member.name + "#" + str(member.discriminator), inline=True)
                unban_embed.set_thumbnail(url=member.avatar_url)
                unban_embed.set_footer(icon_url=object_after.icon_url, text=object_after.name)

                await client.send_message(admin_chan, embed=unban_embed)
        except:
            logger.error(traceback.format_exc())

    # Someone joined, check to see if they're in the banpool, if so, ban them.
    if event_type == "member_join":
        try:
            result = banpool_manager.is_user_banned(member.id)

            if result[1]:
                logger.debug('member_join was caught for banpool ID: {}'.format(member.id))
                user_id = member.id
                user_name = member.name
                user_discriminator = member.discriminator
                user_avatar_url = member.avatar_url
                server_id = member.server.id
                server_icon_url = member.server.icon_url
                server_name = member.server.name

                is_exception = banpool_manager.is_user_in_exceptions(user_id, server_id)

                if not is_exception:
                    logger.debug('member joined is in the banpool and has no exceptions: {}'.format(member.id))
                    ban_embed = Embed(title="User Banned on Join", color=Color.green())
                    ban_embed.add_field(name="Server ID", value=server_id, inline=True)
                    ban_embed.add_field(name="User ID", value=user_id, inline=True)
                    ban_embed.add_field(name="User Name", value=user_name + "#" + str(user_discriminator), inline=True)
                    ban_embed.set_thumbnail(url=user_avatar_url)
                    ban_embed.set_footer(icon_url=server_icon_url, text=server_name)

                    await client.ban(member)
                    await client.send_message(admin_chan, embed=ban_embed)
        except:
            logger.error(traceback.format_exc())
