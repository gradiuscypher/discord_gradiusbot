import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <debug_logger.py> When activated, stores debug message details.")

debug_enabled = None


async def action(**kwargs):
    """
    [gradiusbot]
    owner_id =
    public_debug =
    """
    global debug_enabled

    message = kwargs['message']
    config = kwargs['config']

    owner_id = config.getint('gradiusbot', 'owner_id')

    if debug_enabled is None:
        debug_enabled = config.getboolean('gradiusbot', 'public_debug')

    split_message = message.content.split()

    if len(split_message) > 0:
        if message.author.id == owner_id and split_message[0] == 'public-debug-on':
            debug_enabled = True
            await message.channel.send("Public debug message logging has been ENABLED.")

        elif message.author.id == owner_id and split_message[0] == 'public-debug-off':
            debug_enabled = False
            await message.channel.send("Public debug message logging has been DISABLED.")

        else:
            if debug_enabled:
                role_list = [role.name for role in message.author.roles]

                log_json = {
                    'log_type': 'public_debug',
                    'author.id': message.author.id,
                    'author.name': message.author.name,
                    'author.discriminator': message.author.discriminator,
                    'message_id': message.id,
                    'channel.name': message.channel.name,
                    'channel.id': message.channel.id,
                    'guild.name': message.guild.name,
                    'guild.id': message.guild.id,
                    'roles': role_list
                }
                logger.debug(message.content, extra=log_json)
