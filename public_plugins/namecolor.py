import configparser
import asyncio

print("[Public Plugin] <namecolor.py>: This plugin lets users change their namecolor.")

config = configparser.RawConfigParser()
config.read('config.conf')


@asyncio.coroutine
def action(message, client):
    if message.channel.name == config.get('BotSettings', 'bot_channel'):
        split_content = message.content.split()

        if split_content[0] == "namecolor":
            server = message.server

            # Build a list of available roles that are namecolors
            avail_colors = {}
            for r in server.roles:
                split_name = r.name.split('_')

                if split_name[0] == "namecolor":
                    avail_colors[split_name[1]] = r

            if len(split_content) == 2:
                if split_content[1] in avail_colors.keys():
                    for role in message.author.roles:
                        if role.name.split("_")[0] == "namecolor":
                            yield from client.remove_roles(message.author, role)
                    yield from client.add_roles(message.author, avail_colors[split_content[1]])
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
