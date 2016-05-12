import asyncio
import traceback
import logging
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)


@asyncio.coroutine
def action(message, client, config):
    try:
        author = str(message.author)
        content = message.clean_content
        server = str(message.server)
        channel = str(message.channel)
        timestamp = datetime.utcnow()
        author_id = str(message.author.id)

        logger.debug("{} {} {} {} {} {}".format(timestamp, server, channel, author_id, author, content))

    except:
        traceback.print_exc()
