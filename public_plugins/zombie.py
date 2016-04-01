import asyncio
import discord

print("[Public Plugin] <zombie.py>: This plugin lets you do zombie things.")

bite_cd_value = 8
bite_time = 2


@asyncio.coroutine
def action(message, client, config):
    is_zombie = discord.utils.get(message.author.roles, name="zombie")
    zombie_role = discord.utils.get(message.server.roles, name="zombie")

    if is_zombie is not None:
        bite_cd = discord.utils.get(message.author.roles, name="bite_cd")

        message_mentions = message.mentions
        split_content = message.clean_content.split()
        if len(split_content) >= 2 and len(message_mentions) == 1:
            if split_content[0] == "bite" and bite_cd is None:
                bite_cd_role = discord.utils.get(message.server.roles, name="bite_cd")
                # yield from client.send_message(message.channel, message.author.name + " tries to bite " + split_content[1] + "!")
                print("{} biting {}".format(message.author.name, split_content[1]))
                yield from asyncio.sleep(bite_time)

                is_target_blocking = discord.utils.get(message_mentions[0].roles, name="blocking")

                if is_target_blocking is None:
                    # yield from client.send_message(message.channel, message.author.name + " bit " + split_content[1] + "!")
                    yield from client.add_roles(message_mentions[0], zombie_role)
                else:
                    yield from client.send_message(message.channel, split_content[1] + " blocked " + message.author.name + "'s attack!")

                yield from client.add_roles(message.author, bite_cd_role)
                yield from asyncio.sleep(bite_cd_value)
                yield from client.remove_roles(message.author, bite_cd_role)
