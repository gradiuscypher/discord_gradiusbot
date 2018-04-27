import asyncio
import discord

print("[Event Plugin] <streamer_grouper.py>: This plugin places streaming users into a specific group.")


@asyncio.coroutine
def action(message, client, config, event_type, object_after=None):
    if event_type == 'member_update':
        role = discord.utils.get(message.server.roles, name="streaming")
        is_streaming = discord.utils.get(message.roles, name="streaming")

        if is_streaming is None and object_after.game is not None:
            if object_after.game.url is not None:
                yield from client.add_roles(message, role)

        if is_streaming is not None and object_after.game is not None:
            if object_after.game.url is None:
                yield from client.remove_roles(message, role)

        if is_streaming is not None and object_after.game is None:
            yield from client.remove_roles(message, role)
