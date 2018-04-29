import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Relationship Event Plugin] <example_relationship_event_plugin.py>: This plugin shows you how to use relationship events.")


@asyncio.coroutine
async def action(**kwargs):
    event_type = kwargs['event_type']

    if event_type == 'relationship.add':
        relationship = kwargs['relationship']
        print("The user {} has requested a relationship.".format(relationship.user.name))
        await relationship.accept()
    if event_type == 'relationship.remove':
        relationship = kwargs['relationship']
        print("The user {} has removed the relationship.".format(relationship.user.name))
    if event_type == 'relationship.update':
        before = kwargs['before']
        after = kwargs['after']
        print("The relationship has been updated.\n\nbefore:{}\n\nafter:{}".format(before, after))
