import logging
import discord.utils

logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <recon.py> recon.")

debug_enabled = None


async def action(**kwargs):
    """
    [gradiusbot]
    owner_id =
    """
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    split_message = [s.lower() for s in message.content.split()]

    if len(split_message) == 2:
        if split_message[0] == '!recon':
            target_guild = discord.utils.get(client.guilds, id=int(split_message[1]))
            if target_guild:
                for t_channel in target_guild.channels:
                    print(f"[{t_channel.name}] - {t_channel.changed_roles}")
