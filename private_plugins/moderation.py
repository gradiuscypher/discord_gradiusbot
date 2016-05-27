from libs.server_management import ServerManagement
import asyncio
import discord


print("[Private Plugin] <moderation.py>: This plugin provides moderation tools.")

help_message = """
__*moderation help*__
Always use the full user name including unique ID.

!mod punish USERNAME REASON_MESSAGE

!mod timeout USERNAME REASON_MESSAGE

!mod ban USERNAME REASON_MESSAGE
"""

sm = ServerManagement()


@asyncio.coroutine
def action(message, client, config):
    required_group = config.get('BotSettings', 'mod_group')
    author_id = message.author.id
    split_content = message.content.split()
    default_server = sm.get_default_server(author_id)
    target_server = client.get_server(default_server)

    if split_content[0] == '!mod':
        if target_server is None:
            yield from client.send_message(message.author, "Please set your default server ID with !server before using this command.")
        else:
            target_user = target_server.get_member(message.author.id)

            is_mod = False

            for r in target_user.roles:
                if required_group == r.name:
                    is_mod = True

            if is_mod:
                if len(split_content) >= 4:
                    punished_user_name = split_content[2].split("#")[0]
                    punished_user_discriminator = split_content[2].split("#")[1]
                    mod_message = " ".join(split_content[3:])
                    punished_user = discord.utils.get(target_server.members, name=punished_user_name, discriminator=punished_user_discriminator)

                    if punished_user is not None:
                        if split_content[1] == "punish":
                            # Auto scaling punishment for breaking a rule. Escalates up the moderation punishment scale.
                            # Send message to moderation_log about punishment and details
                            # Send message to offender about punishment details
                            # Execute punishment
                            yield from client.send_message(message.author, "I'mma punish {} for you with the message {}".format(punished_user.name, mod_message))
                        elif split_content[1] == "timeout":
                            # Auto scaling timeout for breaking a rule. Escalates up the moderation timeout scale.
                            # Send message to moderation_log about punishment and details
                            # Send message to offender about punishment details
                            # Execute punishment
                            yield from client.send_message(message.author, "I'mma timeout {} for you with the message {}".format(punished_user.name, mod_message))
                        elif split_content[1] == "ban":
                            # Instant permaban for instances where it's required
                            # Send message to moderation_log about punishment and details
                            # Send message to offender about punishment details
                            # Execute punishment
                            yield from client.send_message(message.author, "I'mma ban {} for you with the message {}".format(punished_user.name, mod_message))
                        else:
                            yield from client.send_message(message.author, "Please verify your command. Use !help")
                    else:
                        yield from client.send_message(message.author, "This user does not exist on your default server, please verify your server and target user.")

