from libs.server_management import ServerManagement
import asyncio
import discord
import traceback


print("[Private Plugin] <servers.py>: This plugin lists the servers and their IDs for command interaction.")

help_message = """
__**!servers help** (PM Only)__

List the servers that you and the bots have in common. These are the servers use can use commands with.

Examples:
!servers
Lists the servers you share with the bot, and gives you their ID.

!servers set SERVER_NUMBER
Sets the default server ID so you don't have to type it every time for commands related to servers.

"""

sm = ServerManagement()


@asyncio.coroutine
def action(message, client, config):
    servers = []
    server_index = []
    target_user_id = message.author.id
    for server in client.servers:
        user = discord.utils.get(server.members, id=target_user_id)
        if user is not None:
            servers.append(server)

    split_content = message.content.split()

    if split_content[0] == '!servers':
        s_index = 0
        msg_string = ""

        for server in servers:
            msg_string += "{}) {}    [{}]\n".format(s_index, server.name, server.id)
            server_index.append(s_index)
            s_index += 1

        if len(split_content) == 1:
            default_server = sm.get_default_server(target_user_id)

            if default_server is None and len(servers) > 0:
                sm.set_default_server(target_user_id, servers[0].id)
                yield from client.send_message(message.author, "I've set your default server to {}".format(servers[0].name))

            yield from client.send_message(message.author, "Your default server ID is: {}".format(sm.get_default_server(target_user_id)))
            yield from client.send_message(message.author, msg_string)

        elif len(split_content) == 3:
            if split_content[1] == "set":
                try:
                    selected_id = int(split_content[2])

                    if selected_id in server_index:
                        sm.set_default_server(target_user_id, servers[selected_id].id)
                        yield from client.send_message(message.author, "I've set your default server to {}".format(servers[selected_id]))
                    else:
                        print("failed to find server id")
                        yield from client.send_message(message.author, "You've provided an invalid server number.")
                        yield from client.send_message(message.author, "Use `!servers` to see a list of servers that you can configure.\nPlease pick the number of the server you'd like to use.")
                except:
                    print(traceback.format_exc())
                    yield from client.send_message(message.author, "You've provided an invalid server number.")
                    yield from client.send_message(message.author, "Use `!servers` to see a list of servers that you can configure.\nPlease pick the number of the server you'd like to use.")

            else:
                yield from client.send_message(message.author, "Please make sure your command format is correct. Use `!help` for help.")
                yield from client.send_message(message.author, "Use `!servers` to see a list of servers that you can configure.")
                yield from client.send_message(message.author, "Use `!servers set NUMBER` to set your server to that number.")

        else:
            yield from client.send_message(message.author, "Please make sure your command format is correct. Use `!help` for help.")
            yield from client.send_message(message.author, "Use `!servers` to see a list of servers that you can configure.")
            yield from client.send_message(message.author, "Use `!servers set NUMBER` to set your server to that number.")

