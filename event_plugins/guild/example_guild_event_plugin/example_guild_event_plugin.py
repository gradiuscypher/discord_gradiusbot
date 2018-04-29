import asyncio
import logging

logger = logging.getLogger('gradiusbot')

logger.info("[Guild Event Plugin] <example_guild_event_plugin.py>: This plugin shows you how to use guild events.")


@asyncio.coroutine
async def action(event_type, inital_object, config, after=None):
    if event_type == 'create_inital_object':
        print("The {} inital_object was created in {} server.".format(inital_object.name, inital_object.guild.name))
    if event_type == 'delete_inital_object':
        print("The {} inital_object was deleted in {} server.".format(inital_object.name, inital_object.guild.name))
    if event_type == 'inital_object_update' and after:
        print("A inital_object was updated on {} server.\n\nbefore:{}\n\nafter:{}".format(inital_object.guild.name, inital_object, after))
    if event_type == 'pin_update':
        print("{} on {} server had a pin update. Last pin was: {}".format(inital_object.name, inital_object.guild.name, after))
    if event_type == 'guild_update':
        print("{} guild has updated.\n\nbefore:{}\n\nafter:{}".format(inital_object.name, inital_object, after))
    if event_type == 'guild_role_create':
        print("{} guild has created the role {}".format(inital_object.guild.name, inital_object.name))
    if event_type == 'guild_role_delete':
        print("{} guild has deleted the role {}".format(inital_object.guild.name, inital_object.name))
    if event_type == 'guild_role_update':
        print("{} guild has updated a role.\n\nbefore:{}\n\nafter:{}".format(inital_object.guild.name, inital_object, after))
