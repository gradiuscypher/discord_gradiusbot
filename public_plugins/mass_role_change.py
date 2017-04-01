import asyncio
import discord

print("[Public Plugin] <mass_role_change.py>: Assigns roles to everyone.")


@asyncio.coroutine
def action(message, client, config):
    split_content = message.content.split()
    bot_channel = config.get("BotSettings", "bot_channel")
    role = discord.utils.get(message.server.roles, name="Kanye Fan")

    if str(message.author) == "Dev#0329":
        if split_content[0] == "!addrole" and message.channel.name == bot_channel:
            members = message.server.members
            for m in members:
                yield from client.add_roles(m, role)
        elif message.content == "!removerole":
            members = message.server.members
            for m in members:
                yield from client.remove_roles(m, role)

