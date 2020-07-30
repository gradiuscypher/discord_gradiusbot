import logging
import json

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <url_checker.py> Checks to see if a URL is allowed on a server.")


with open('public_plugins/url_checker/url_checker.json') as url_file:
    blocked_urls = json.load(url_file)


async def action(**kwargs):
    """
    """
    message = kwargs['message']

    for url in blocked_urls:
        if url in message.content:
            await message.delete()
