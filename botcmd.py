#!/usr/bin/env python

import argparse
import json
from libs.discord_libs.discord_libs import DiscordLibs


parser = argparse.ArgumentParser()

parser.add_argument("bot_id", help="Bot ID")
parser.add_argument("bot_token", help="Bot Token")
parser.add_argument("--all", help="Show all configuration information about the bot.", action="store_true")
parser.add_argument("--guilds", help="List servers the bot is a part of.", action="store_true")
parser.add_argument("--loglevel", help="Python log level for DiscordLibs. By default uses INFO")
parser.add_argument("--logtofile", help="Log to a file")
args = parser.parse_args()

if args.logtofile:
    log_to_file = True
else:
    log_to_file = False

if args.loglevel:
    log_level = args.loglevel
else:
    log_level = "INFO"

dlibs = DiscordLibs(args.bot_id, args.bot_token, log_to_file=log_to_file, log_level=log_level)


def format_guilds():
    guild_list = dlibs.get_current_guilds()

    print("=== Guilds ===")
    for guild in guild_list:
        print("Name: {} | ID: {} | Permissions: {}".format(guild['name'], guild['id'], guild['permissions']))
        print()


def format_user():
    user = dlibs.get_current_user()

    print("=== User ===")
    print("Username: {} | Discriminator: {} | ID: {}".format(user['username'], user['discriminator'], user['id']))
    print()


def format_guild_roles():
    guild_list = dlibs.get_current_guilds()

    print("=== Guild Roles ===")
    for guild in guild_list:
        print("--- {} ---".format(guild['name']))
        roles = dlibs.get_guild_roles(guild['id'])

        for role in roles:
            print("Name: {} | ID: {}".format(role['name'], role['id']))
        print()

if args.all:
    format_guilds()
    format_user()
    format_guild_roles()

if args.guilds:
    format_guilds()
