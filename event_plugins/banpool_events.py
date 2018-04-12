import asyncio
import discord
from libs import banpool
from discord import Embed, Color

print("[Event Plugin] <banpool_events.py>: This plugin manages banpool related events.")

banpool_manager = banpool.BanPoolManager()


# NOTE: In this case object_after is the server
@asyncio.coroutine
async def action(member, client, config, event_type, object_after=None):
    admin_server_id = config.get('banpool', 'admin_server_id')
    admin_chan_name = config.get('banpool', 'admin_chan')
    admin_server = discord.utils.get(client.servers, id=admin_server_id)
    admin_chan = discord.utils.get(admin_server.channels, name=admin_chan_name)

    # Someone was unbanned, check to see if they're in the banpool, if so, add an exception for this server
    if event_type == "member_unban":
        result = banpool_manager.is_user_banned(member.id)

        # User is in banpool, so we need to add an exception
        if result[1]:
            banpool_manager.add_user_to_exceptions(member.id, object_after.id)

            unban_embed = Embed(title="User Exception Added", color=Color.orange())
            unban_embed.add_field(name="Server ID", value=object_after.id, inline=True)
            unban_embed.add_field(name="User ID", value=member.id, inline=True)
            unban_embed.add_field(name="User Name", value=member.name + "#" + str(member.discriminator), inline=True)
            unban_embed.set_thumbnail(url=member.avatar_url)
            unban_embed.set_footer(icon_url=object_after.icon_url, text=object_after.name)

            await client.send_message(admin_chan, embed=unban_embed)
