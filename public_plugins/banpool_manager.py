import asyncio
from libs import banpool

print("[Public Plugin] <echo.py>: This plugin echoes stuff to a public channel.")

banpool_manager = banpool.BanPoolManager()


@asyncio.coroutine
async def action(message, client, config):
    """
    Config Values:
    [banpool]
    # The Discord ID of the Admin user
    admin_id =

    :param message: discord message obj
    :param client: discord client obj
    :param config: config obj
    :return:
    """

    # get config values
    admin_id = config.get('banpool', 'admin_id')

    author_id = message.author.id

    if author_id == admin_id:
        split_content = message.content.split()

        if split_content[0] == '!banpool':
            if split_content[1] == 'list':
                pass
            if split_content[1] == 'listusers':
                pass
            if split_content[1] == 'adduser':
                pass
            if split_content[1] == 'adduserlist':
                pass
            if split_content[1] == 'listexception':
                pass
            if split_content[1] == 'addexception':
                pass
            if split_content[1] == 'removeuser':
                pass
            if split_content[1] == 'removeexception':
                pass
