import configparser
import discord.utils

# Setup config
config = configparser.RawConfigParser()
config.read("config.conf")
admin_name = config.get("Permissions", "admin_group")


def has_admin(member):
    """
    Returns function if member has admin
    :param function:
    :return:
    """
    return discord.utils.get(member.roles, name=admin_name)
