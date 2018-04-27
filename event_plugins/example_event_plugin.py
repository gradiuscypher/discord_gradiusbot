import asyncio
import discord

print("[Event Plugin] <example_event_plugin.py>: This plugin shows you how to use events.")


@asyncio.coroutine
def action(message, client, config, event_type, object_after=None):

    if event_type == "delete":
        yield from client.send_message(message.channel, "Deleted: " + ' '.join(message.attachments))
        print(repr(message.attachments))
    if event_type == "edit":
        yield from client.send_message(message.channel, "Edited:\n " + "- " + message.content +
                                       "\n+ " + object_after.content)

    if event_type == 'member_update':
        role = discord.utils.get(message.server.roles, name="streaming")
        is_streaming = discord.utils.get(message.roles, name="streaming")

        if is_streaming is None and object_after.game is not None:
            if object_after.game.url is not None:
                print("PUT ME IN COACH")
                yield from client.add_roles(message, role)

        if is_streaming is not None and object_after.game is not None:
            if object_after.game.url is None:
                print("TAKE ME OUT COACH, IM NOT STREAMING")
                yield from client.remove_roles(message, role)

        if is_streaming is not None and object_after.game is None:
            print("TAKE ME OUT COACH, IM NOT GAMING")
            yield from client.remove_roles(message, role)
