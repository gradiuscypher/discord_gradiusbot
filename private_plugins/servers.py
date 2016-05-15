import asyncio
import discord


print("[Private Plugin] <servers.py>: This plugin lists the servers and their IDs for command interaction.")

help_message = """
__*servers help*__

List the servers that you and the bots have in common. These are the servers use can use commands with.

Examples:
!servers

"""


@asyncio.coroutine
def action(message, client, config):
    servers = []
    target_user_id = message.author.id
    for server in client.servers:
        user = discord.utils.get(server.members, id=target_user_id)
        if user is not None:
            servers.append(server)

    split_content = message.content.split()

    if split_content[0] == '!servers':
        if len(split_content) != 1:
            yield from client.send_message("Please make sure your command format is correct. Use !help for help.")
            yield from client.send_message("Use !servers to see a list of servers that you can configure.")

        else:
                msg_string = ""

                for server in servers:
                    msg_string += "ID: {} Name: {}\n".format(server.id, server.name)

                yield from client.send_message(message.author, msg_string)
