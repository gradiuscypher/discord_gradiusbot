import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Public Plugin] <portals.py>: This plugin allows you to use portals to move your messages around!")

portal_dict = {}


@asyncio.coroutine
async def action(**kwargs):
    message = kwargs['message']
    config = kwargs['config']
    client = kwargs['client']

    # if the portal is blue, store a key:value of user:portal content
    if '<:portal_blue:502160330911121428>' in message.content:
        remaining_content = message.content.replace('<:portal_blue:502160330911121428>', '')
        portal_dict[message.author.id] = {"content": remaining_content, "message": message}

    # if the portal is red, check to see if the user has any blue portals, and move the content from there, to here.
    if '<:portal_red:502160345293520907>' in message.content:
        if message.author.id in portal_dict.keys() and portal_dict[message.author.id]:
            await message.channel.send('<@' + str(message.author.id) + '>: <:portal_red:502160345293520907>' + portal_dict[message.author.id]['content'])
            await portal_dict[message.author.id]['message'].delete()
            await message.delete()
            portal_dict[message.author.id] = None
