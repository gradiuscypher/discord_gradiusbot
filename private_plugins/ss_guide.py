import asyncio
from libs.link_keeper import LinkKeeper


lk = LinkKeeper()

note = """
NOTE: This plugin is written to be used on a bot that is only in a single server.
This plugin will not function properly on a bot that's a member of more than one server.
"""

print("[Private Plugin] <ss_guide.py>: This plugin allows users to look up and add guides/links along with tags.")
print("[Private Plugin] {}".format(note))

help_message = """
__*guide help*__

**!guide**- show this text

**!guide all**- show all useful links

**!guide search** __*tag*__- show all guides tagged with given tag

**!guide add** __*link*__ __*description*__- add a guide with the given link and description. Must have permissions.

**!guide delete** __*guideid*__- delete a guide with the given id. Must have permissions.

**!guide tag** __*guideid*__ __*tag*__- tag a given guide id with given tag. Must have permissions.

**!guide untag** __*guideid*__ __*tag*__- remove given tag from given guide id. Must have permissions.
"""


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()
    server_id = config.get('BotSettings', 'server_id')
    required_group = config.get('BotSettings', 'guide_group')
    server = client.get_server(server_id)
    target_user = server.get_member(message.author.id)
    guider = False

    for r in target_user.roles:
        if required_group == r.name:
            guider = True

    if len(split_content) > 0:
        if split_content[0] == "!guide":
            if len(split_content) > 1:
                if split_content[1] == 'all':
                    links = lk.get_all_links()
                    reply = "__All Guides__:\n"
                    for link in links:
                        tag_line = "        Tags: "
                        reply += str(link.id) + ". " + link.link + " : \"" + link.description + "\"\n"
                        for tag in link.tags:
                            tag_line += "*" + tag.tag_text + "* "
                        reply += tag_line + "\n"
                    yield from client.send_message(message.author, reply)

                if split_content[1] == 'search':
                    if len(split_content) == 3:
                        links = lk.get_link(split_content[2])
                        reply = "__" + split_content[2] + " Guides__:\n"
                        for link in links:
                            tag_line = "        Tags: "
                            reply += str(link.id) + ". " + link.link + " : \"" + link.description + "\"\n"
                            for tag in link.tags:
                                tag_line += "*" + tag.tag_text + "* "
                            reply += tag_line + "\n"
                        yield from client.send_message(message.author, reply)
                    else:
                        yield from client.send_message(message.author, "Not the right number of arguments for this command.")

                if split_content[1] == 'add':
                    if guider:
                        if len(split_content) > 4:
                            link = split_content[2]
                            description = ' '.join(split_content[3:])
                            lk.add_link(link, description)
                            yield from client.send_message(message.author, "Your link has been added.")
                    else:
                        yield from client.send_message(message.author, "You don't have permissions.")

                if split_content[1] == 'delete':
                    if guider:
                        if len(split_content) == 3:
                            lk.remove_link(split_content[2])
                            yield from client.send_message(message.author, "The guide has been deleted.")
                        else:
                            yield from client.send_message(message.author, "Not the right number of arguments for this command.")
                    else:
                        yield from client.send_message(message.author, "You don't have permissions.")

                if split_content[1] == 'tag':
                    if guider:
                        if len(split_content) == 4:
                            lk.add_tag(split_content[2], split_content[3])
                            yield from client.send_message(message.author, "The guide has been tagged.")
                        else:
                            yield from client.send_message(message.author, "Not the right number of arguments for this command.")
                    else:
                        yield from client.send_message(message.author, "You don't have permissions.")

                if split_content[1] == 'untag':
                    if guider:
                        if len(split_content) == 4:
                            lk.remove_tag(split_content[2], split_content[3])
                            yield from client.send_message(message.author, "The guide has been untagged.")
                        else:
                            yield from client.send_message(message.author, "Not the right number of arguments for this command.")
                    else:
                        yield from client.send_message(message.author, "You don't have permissions.")
            else:
                yield from client.send_message(message.author, help_text)
