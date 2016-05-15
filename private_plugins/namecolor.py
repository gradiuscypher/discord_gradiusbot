import asyncio
import random
import discord


print("[Private Plugin] <namecolor.py>: This plugin sets the namecolor of the user via PM.")

help_message = """
__*namecolor help*__

ID - server ID you want to set your name color on.

**!namecolor** *color* ID- grants your user a different color name.
**!namecolor list**  ID - see the list of namecolors.
**!namecolor random** ID - pick a random namecolor.

Examples:
!namecolor red 126410825685663744
!namecolor list 126410825685663744

If your desired color does not exist, speak to a chat admin.
"""


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()

    if split_content[0] == '!namecolor':
        if len(split_content) != 3:
            yield from client.send_message(message.author, "Please make sure your command format is correct. Use !help for help.")
            yield from client.send_message(message.author, "Use !servers to see a list of servers that you can configure.")

        else:
            target_server = client.get_server(split_content[2])

            if target_server is None:
                yield from client.send_message(message.author, "Invalid server ID. Use !servers for a list of server IDs.")

            else:
                new_roles = []
                server = target_server
                target_user = server.get_member(message.author.id)

                # Build a list of available roles that are namecolors
                avail_colors = {}
                for r in server.roles:
                    split_name = r.name.split('_')

                    if split_name[0] == "namecolor":
                        avail_colors[split_name[1]] = r

                if split_content[1].lower() in avail_colors.keys():
                    for role in target_user.roles:
                        if not role.name.split("_")[0] == "namecolor":
                            new_roles.append(role)

                    yield from client.replace_roles(target_user, *new_roles)
                    yield from asyncio.sleep(.5)
                    yield from client.add_roles(target_user, avail_colors[split_content[1].lower()])
                    yield from client.send_message(message.author, "Adding your new name color.")

                elif split_content[1].lower() == "random":
                    for role in target_user.roles:
                        if not role.name.split("_")[0] == "namecolor":
                            new_roles.append(role)

                    yield from client.replace_roles(target_user, *new_roles)
                    yield from asyncio.sleep(.5)
                    yield from client.add_roles(target_user, avail_colors[random.choice(list(avail_colors.keys()))])
                    yield from client.send_message(message.author, "Adding your new name color.")

                elif split_content[1].lower() == "list":
                    name_color_str = ""
                    for color in avail_colors.keys():
                        name_color_str += color + "\n"
                    yield from client.send_message(message.author, "Available name colors: " + name_color_str)

                else:
                    name_color_str = ""
                    for color in avail_colors.keys():
                        name_color_str += color + "\n"

                    yield from client.send_message(message.author, "Please select a valid namecolor.")
                    yield from client.send_message(message.author, "Available name colors:\n" + name_color_str)
