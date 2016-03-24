import asyncio

note = """
NOTE: This plugin is written to be used on a bot that is only in a single server.
This plugin will not function properly on a bot that's a member of more than one server.
"""

print("[Private Plugin] <ss_optional_groups.py>: This plugin sets the optional groups of the user via PM.")
print("[Private Plugin] {}".format(note))


@asyncio.coroutine
def action(message, client, config):
    server_id = config.get('BotSettings', 'server_id')
    server = client.get_server(server_id)
    target_user = server.get_member(message.author.id)
    optional_groups = {}
    new_roles = []

    split_content = message.content.split()

    if len(split_content) > 0:
        if split_content[0] == "!join" or split_content[0] == "!leave":

            for r in server.roles:
                split_name = r.name.split('_')

                if split_name[0] == "opt":
                    optional_groups[split_name[1]] = r

        if split_content[0] == "!join":
            if len(split_content) == 2:
                if split_content[1].lower() in optional_groups.keys():
                    yield from client.add_roles(target_user, optional_groups[split_content[1].lower()])
                    yield from client.send_message(message.author, "Adding you to the group.")

            else:
                yield from client.send_message(message.author, "!join groupname or !leave groupname")
                groups_str = ""
                for group in optional_groups.keys():
                    groups_str += group + " "
                yield from client.send_message(message.author, "Available groups: " + groups_str)

        if split_content[0] == "!leave":
            if len(split_content) == 2:
                if split_content[1].lower() in optional_groups.keys():
                    for role in target_user.roles:
                        role_split = role.name.split("_")
                        if len(role_split) > 1:
                            if not role_split[1] == split_content[1].lower():
                                new_roles.append(role)
                        else:
                            new_roles.append(role)

                    yield from client.replace_roles(target_user, *new_roles)
                    yield from client.send_message(message.author, "Removing you from the group.")

            else:
                yield from client.send_message(message.author, "!join groupname or !leave groupname")
                groups_str = ""
                for group in optional_groups.keys():
                    groups_str += group + " "
                yield from client.send_message(message.author, "Available groups: " + groups_str)
