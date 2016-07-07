from libs.server_management import ServerManagement
import asyncio
import random

sm = ServerManagement()

print("[Private Plugin] <namecolor.py>: This plugin sets the namecolor of the user via PM.")

help_message = """
__**!namecolor help**__

!namecolor *color* - grants your user a different color name.
!namecolor list - see the list of namecolors.
!namecolor random - pick a random namecolor.

Examples:
!namecolor red
!namecolor list

If your desired color does not exist, speak to a chat admin.
"""


@asyncio.coroutine
def action(message, client, config):
    author_id = message.author.id
    split_content = message.content.split()
    default_server = sm.get_default_server(author_id)
    target_server = client.get_server(default_server)

    if split_content[0] == '!namecolor':
        if target_server is None:
            yield from client.send_message(message.author, "Please set your default server ID with !servers before using this command.")

        if len(split_content) != 2:
            yield from client.send_message(message.author, "Please make sure your command format is correct. Use !help for help.")

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
