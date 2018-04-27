import asyncio
import random
import discord

print("[Public Plugin] <namecolor.py>: This plugin lets users change their namecolor.")


@asyncio.coroutine
def action(message, client, config):

    if message.author.name == "gradius" and message.content == "nuke":
        all_members = message.server.members

        for member in all_members:
            namecolor = discord.utils.find(lambda r: r.name.split('_')[0] == "namecolor", member.roles)
            if namecolor is not None:
                print("{} is {}".format(member.name, namecolor.name))
                yield from asyncio.sleep(1)
                yield from client.remove_roles(member, namecolor)
