from libs.server_management import ServerManagement
from libs.moderation import Moderation
import asyncio
import discord


print("[Private Plugin] <moderation.py>: This plugin provides moderation tools.")

help_message = """
__**!mod help**__
Always use the full user name including unique ID.

!mod punish USERNAME REASON_MESSAGE

!mod timeout USERNAME REASON_MESSAGE

!mod ban USERNAME REASON_MESSAGE
"""

sm = ServerManagement()
moderation = Moderation()


@asyncio.coroutine
def action(message, client, config):
    required_group = config.get('AdminSettings', 'mod_group')
    author_id = message.author.id
    split_content = message.content.split()
    default_server = sm.get_default_server(author_id)
    target_server = client.get_server(default_server)

    if split_content[0] == '!mod':
        if target_server is None:
            yield from client.send_message(message.author, "Please set your default server ID with !servers before using this command.")
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
                            """
                            ## Punishment tiers
                                1. Warning via PM with REASON_MESSAGE
                                2. 1 hour kick+ban from chat
                                3. 24 hour kick+ban from chat
                                4. 3 day kick+ban from chat
                                5. 7 day kick+ban from chat
                                6. 15 day kick+ban from chat
                                7. 30 day kick+ban from chat
                                8. 30 day kick+ban and account marked for perma-ban review
                            """
                            # Update Moderation databases
                            moderation.punish(punished_user.id, punished_user.name, mod_message, message.author.id,
                                              message.author.name)

                            # Send message to moderation_log about punishment and details
                            punish_message = "**Punishment**\n**User:** {}\n**UserID:** {}\n**Reason:** {}" \
                                             "\n**Moderator:** {}".format(punished_user_name, punished_user.id,
                                                                          mod_message, message.author.name)
                            # TODO: Change this to send to moderation channel
                            yield from client.send_message(message.author, punish_message)

                            # Send message to offender about punishment details
                            # Execute punishment
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

