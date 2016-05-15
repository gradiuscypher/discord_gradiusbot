import asyncio
import random

note = """
NOTE: This plugin is written to be used on a bot that is only in a single server.
This plugin will not function properly on a bot that's a member of more than one server.
"""

print("[Private Plugin] <ss_namecolor.py>: This plugin sets the namecolor of the user via PM.")
print("[Private Plugin] {}".format(note))

help_message = """
__*namecolor help*__

**!namecolor** *color* - grants your user a different color name.
                    Use it without a color to see a list of colors.

                    If your desired color does not exist, speak to a chat admin.

                    You can also use **!namecolor** *random* to pick a random color.
"""


@asyncio.coroutine
def action(message, client, config):
    new_roles = []
    server_id = config.get('BotSettings', 'server_id')
    server = client.get_server(server_id)
    target_user = server.get_member(message.author.id)

    split_content = message.content.split()

    if len(split_content) > 0:
        if split_content[0] == "!namecolor":

            # Build a list of available roles that are namecolors
            avail_colors = {}
            for r in server.roles:
                split_name = r.name.split('_')

                if split_name[0] == "namecolor":
                    avail_colors[split_name[1]] = r

            if len(split_content) == 2:
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

                else:
                    yield from client.send_message(message.author, "namecolor command format: namecolor [color]")
                    name_color_str = ""
                    for color in avail_colors.keys():
                        name_color_str += color + " "
                    yield from client.send_message(message.author, "Available name colors: " + name_color_str)

            else:
                yield from client.send_message(message.author, "namecolor command format: namecolor [color]")
                name_color_str = ""
                for color in avail_colors.keys():
                    name_color_str += color + " "
                yield from client.send_message(message.author, "Available name colors: " + name_color_str)

