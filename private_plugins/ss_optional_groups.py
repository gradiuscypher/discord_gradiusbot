import asyncio
import traceback
from datetime import datetime
from libs.elastic_logging import ElasticLogging

elog = ElasticLogging()

note = """
NOTE: This plugin is written to be used on a bot that is only in a single server.
This plugin will not function properly on a bot that's a member of more than one server.
"""

print("[Private Plugin] <ss_optional_groups.py>: This plugin sets the optional groups of the user via PM.")
print("[Private Plugin] {}".format(note))


@asyncio.coroutine
def action(message, client, config):
    try:
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
                        groups_str += group + "\n"
                    yield from client.send_message(message.author, "**Available groups:**\n" + groups_str)

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
                    current_roles = {}
                    for r in target_user.roles:
                        split_name = r.name.split('_')

                        if split_name[0] == "opt":
                            current_roles[split_name[1]] = r

                    yield from client.send_message(message.author, "!join groupname or !leave groupname")
                    groups_str = ""
                    for group in current_roles.keys():
                        groups_str += group + "\n"
                    yield from client.send_message(message.author, "**Available groups:**\n" + groups_str)
    except:
        server_id = config.get('BotSettings', 'server_id')
        server = client.get_server(server_id)
        target_user = server.get_member(message.author.id)
        author_name = target_user.name
        author_id = target_user.id
        error_message = "Problem executing ss_optional_groups function"
        author_message = message.clean_content
        tb = traceback.print_exc()
        app = "ss_optional_groups.py"
        error_type = "exception"
        timestamp = datetime.now()
        extra_data = ""
        channel = "Private Message"

        elog.log_message(server_id, channel, author_name, author_id, error_message, author_message, tb, app, error_type,
                         timestamp, extra_data)
