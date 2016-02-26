import asyncio
import random

print("[Public Plugin] <namecolor.py>: This plugin lets users change their namecolor.")


@asyncio.coroutine
def action(message, client, config):
    new_roles = []
    bot_channel = config.get("BotSettings", "bot_channel")

    split_content = message.content.split()

    if len(split_content) > 0:
        if split_content[0] == "!namecolor" and message.channel.name == bot_channel:
            server = message.server

            # Build a list of available roles that are namecolors
            avail_colors = {}
            for r in server.roles:
                split_name = r.name.split('_')

                if split_name[0] == "namecolor":
                    avail_colors[split_name[1]] = r

            if len(split_content) == 2:
                if split_content[1].lower() in avail_colors.keys():
                    for role in message.author.roles:
                        if not role.name.split("_")[0] == "namecolor":
                            new_roles.append(role)

                    yield from client.replace_roles(message.author, *new_roles)
                    yield from asyncio.sleep(.5)
                    yield from client.add_roles(message.author, avail_colors[split_content[1].lower()])
                    yield from client.send_message(message.author, "Adding your new name color.")

                elif split_content[1].lower() == "random":
                    for role in message.author.roles:
                        if not role.name.split("_")[0] == "namecolor":
                            new_roles.append(role)

                    yield from client.replace_roles(message.author, *new_roles)
                    yield from asyncio.sleep(.5)
                    yield from client.add_roles(message.author, avail_colors[random.choice(list(avail_colors.keys()))])
                    yield from client.send_message(message.author, "Adding your new name color.")


                else:
                    yield from client.send_message(message.author, "namecolor command format: namecolor [color]")
                    name_color_str = ""
                    for color in avail_colors.keys():
                        name_color_str += color + " "
                    yield from client.send_message(message.author, "Available name colors: " + name_color_str + "\n" +
                                                   "Color screenshot: http://i.imgur.com/ysjlBI6.png")

            else:
                yield from client.send_message(message.author, "namecolor command format: namecolor [color]")
                name_color_str = ""
                for color in avail_colors.keys():
                    name_color_str += color + " "
                yield from client.send_message(message.author, "Available name colors: " + name_color_str + "\n" +
                                                   "Color screenshot: http://i.imgur.com/ysjlBI6.png")

