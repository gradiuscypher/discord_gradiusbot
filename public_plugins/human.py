import asyncio
import discord

print("[Public Plugin] <human.py>: This plugin lets you do human things.")

block_cd_value = 4
block_length = 3
bite_cd_value = 4
reload_length = 1


@asyncio.coroutine
def action(message, client, config):

    message_mentions = message.mentions
    split_content = message.clean_content.split()

    is_zombie = discord.utils.get(message.author.roles, name="zombie")
    bite_cd_role = discord.utils.get(message.server.roles, name="bite_cd")
    blocking_cd_role = discord.utils.get(message.server.roles, name="blocking_cd")

    if is_zombie is None:
        is_blocking = discord.utils.get(message.author.roles, name="blocking")
        is_blocking_cd = discord.utils.get(message.author.roles, name="blocking_cd")
        is_reloading = discord.utils.get(message.author.roles, name="reloading")

        if message.content.lower() == "block" and is_blocking is None and is_blocking_cd is None:
            blocking_role = discord.utils.get(message.server.roles, name="blocking")
            yield from client.add_roles(message.author, blocking_role)
            yield from asyncio.sleep(block_length)
            yield from client.remove_roles(message.author, blocking_role)
            yield from client.add_roles(message.author, blocking_cd_role)
            yield from asyncio.sleep(block_cd_value)
            yield from client.remove_roles(message.author, blocking_cd_role)

        if len(split_content) >= 2 and len(message_mentions) == 1:
            is_zombie = discord.utils.get(message_mentions[0].roles, name="zombie")

            if split_content[0] == "shoot" and is_reloading is None and is_zombie is not None:
                yield from client.add_roles(message_mentions[0], bite_cd_role)
                yield from client.add_roles(message.author, blocking_cd_role)

                yield from asyncio.sleep(reload_length)

                yield from client.remove_roles(message.author, blocking_cd_role)
                yield from asyncio.sleep(bite_cd_value)

                yield from client.remove_roles(message_mentions[0], bite_cd_role)
