from libs.server_management import ServerManagement
import asyncio
import discord


print("[Private Plugin] <moderation.py>: This plugin provides moderation tools.")

help_message = """
__*moderation help*__
INSERT DOCS HERE

!mod punish USERNAME REASON_MESSAGE

!mod timeout USERNAME REASON_MESSAGE

!mod ban USERNAME REASON_MESSAGE
"""

sm = ServerManagement()


@asyncio.coroutine
def action(message, client, config):
    author_id = message.author.id
    split_content = message.content.split()
    target_server = sm.get_default_server(author_id)

    if split_content[0] == '!mod':
        if target_server is None:
            yield from client.send_message(message.author, "Please set your default server ID with !server before using this command.")
        else:
            if len(split_content) == 4:
                if split_content[1] == "punish":
                    mod_message = split_content[2]
                    target_user = split_content[3]
                    # Auto scaling punishment for breaking a rule. Escalates up the moderation punishment scale.
                    # Send message to moderation_log about punishment and details
                    # Send message to offender about punishment details
                    # Execute punishment
                    pass
                elif split_content[1] == "timeout":
                    mod_message = split_content[2]
                    target_user = split_content[3]
                    # Auto scaling timeout for breaking a rule. Escalates up the moderation timeout scale.
                    # Send message to moderation_log about punishment and details
                    # Send message to offender about punishment details
                    # Execute punishment
                    pass
                elif split_content[1] == "ban":
                    mod_message = split_content[2]
                    target_user = split_content[3]
                    # Instant permaban for instances where it's required
                    # Send message to moderation_log about punishment and details
                    # Send message to offender about punishment details
                    # Execute punishment
                    pass
