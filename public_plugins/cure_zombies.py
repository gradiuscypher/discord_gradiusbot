import asyncio
import random
import discord

print("[Public Plugin] <namecolor.py>: This plugin lets users change their namecolor.")


@asyncio.coroutine
def action(message, client, config):

    if message.author.name == "gradius" and message.content == "cure":
        all_members = message.server.members

        for member in all_members:
            is_zombie = discord.utils.get(message.author.roles, name="zombie")
            if is_zombie is not None:
                # yield from client.send_message(message.channel, "Now curing: " + message.author.name)
                print("Now curing {}".format(member.name))
                yield from asyncio.sleep(1)
                yield from client.remove_roles(member, is_zombie)
