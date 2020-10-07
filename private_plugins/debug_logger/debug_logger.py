import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Private Plugin] <debug_logger.py> When activated, stores debug message details.")

debug_enabled = None


async def action(**kwargs):
    """
    [gradiusbot]
    owner_id =
    pm_debug =
    """
    global debug_enabled

    message = kwargs['message']
    config = kwargs['config']

    owner_id = config.getint('gradiusbot', 'owner_id')

    if not debug_enabled:
        debug_enabled = config.getboolean('gradiusbot', 'pm_debug')

    split_message = message.content.split()

    if message.author.id == owner_id and split_message[0] == 'pm-debug-on':
        debug_enabled = True
        await message.channel.send("PM debug message logging has been ENABLED.")

    elif message.author.id == owner_id and split_message[0] == 'pm-debug-off':
        debug_enabled = False
        await message.channel.send("PM debug message logging has been DISABLED.")

    else:
        if debug_enabled:
            log_json = {
                'log_type': 'pm_debug',
                'message.author.id': message.author.id,
                'message.author.name': message.author.name,
                'message.author.discriminator': message.author.discriminator,
                'message.id': message.id
            }
            logger.debug(message.content, extra=log_json)
