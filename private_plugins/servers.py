from libs.server_management import ServerManagement
import asyncio
import discord


print("[Private Plugin] <servers.py>: This plugin lists the servers and their IDs for command interaction.")

help_message = """
__*servers help*__

List the servers that you and the bots have in common. These are the servers use can use commands with.

Examples:
!servers
Lists the servers you share with the bot, and gives you their ID.

!servers set SERVER_ID
Sets the default server ID so you don't have to type it every time for commands related to servers.
"""

sm = ServerManagement()


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
        if len(split_content) == 1:
            msg_string = ""

            for server in servers:
                msg_string += "ID: {} Name: {}\n".format(server.id, server.name)

            yield from client.send_message(message.author, "Your default server ID is: {}".format(sm.get_default_server(target_user_id)))
            yield from client.send_message(message.author, msg_string)

        elif len(split_content) == 3:
            if split_content[1] == "set":
                if split_content[2] in [s.id for s in servers]:
                    sm.set_default_server(target_user_id, split_content[2])
                    yield from client.send_message(message.author, "I've set your default server ID.")
                else:
                    yield from client.send_message(message.author, "You've provided an invalid server ID.")
                    yield from client.send_message(message.author, "Use !servers to see a list of servers that you can configure.")
            else:
                yield from client.send_message(message.author, "Please make sure your command format is correct. Use !help for help.")
                yield from client.send_message(message.author, "Use !servers to see a list of servers that you can configure.")

        else:
            yield from client.send_message(message.author, "Please make sure your command format is correct. Use !help for help.")
            yield from client.send_message(message.author, "Use !servers to see a list of servers that you can configure.")
