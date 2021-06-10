#!/usr/bin/env python

import click
import json
import requests
import traceback
from pprint import pprint

global_url = "https://discord.com/api/v8/applications/{application_id}/commands"
guild_url = "https://discord.com/api/v8/applications/{application_id}/guilds/{guild_id}/commands"
global_command_url = "https://discord.com/api/v8/applications/{application_id}/commands/{command_id}"
guild_command_url = "https://discord.com/api/v8/applications/{application_id}/guilds/{guild_id}/commands/{command_id}"


@click.group()
def cli():
    "Tool for creating Discord Slash commands."


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.argument("command_file", type=click.STRING)
@click.option("--guild_id", type=click.INT, help="The Guild ID for the command. Ommit to make a global command.")
def post(application_id, bot_token, command_file, guild_id=None):
    with open(f'json_commands/{command_file}', 'r') as command_json:
        headers = {
            "Authorization": f"Bot {bot_token}"
        }
        try:
            if guild_id:
                url = guild_url.format(application_id=application_id, guild_id=guild_id)
            else:
                url = global_url.format(application_id=application_id)

            r = requests.post(url, headers=headers, json=json.loads(command_json.read()))
            print(r.status_code)
            pprint(r.json())
        except:
            print(traceback.format_exc())


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.option("--guild_id", type=click.INT, help="The Guild ID for the command. Ommit to make a global command.")
def get(application_id, bot_token, guild_id=None):
    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    try:
        if guild_id:
            url = guild_url.format(application_id=application_id, guild_id=guild_id)
        else:
            url = global_url.format(application_id=application_id)

        r = requests.get(url, headers=headers)
        print(r.status_code)
        pprint(r.json())
    except:
        print(traceback.format_exc())


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("command_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.option("--guild_id", type=click.INT, help="The Guild ID for the command. Ommit to make a global command.")
def delete(application_id, command_id, bot_token, guild_id=None):
    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    try:
        if guild_id:
            url = guild_command_url.format(application_id=application_id, command_id=command_id, guild_id=guild_id)
        else:
            url = global_command_url.format(application_id=application_id, command_id=command_id)

        r = requests.delete(url, headers=headers)
        print(r.status_code)
    except:
        print(traceback.format_exc())


@cli.command()
@click.argument("application_id", type=click.INT)
@click.argument("command_id", type=click.INT)
@click.argument("bot_token", type=click.STRING)
@click.argument("command_file", type=click.STRING)
@click.option("--guild_id", type=click.INT, help="The Guild ID for the command. Ommit to make a global command.")
def patch(application_id, command_id, bot_token, command_file, guild_id=None):
    with open(f'json_commands/{command_file}', 'r') as command_json:
        headers = {
            "Authorization": f"Bot {bot_token}"
        }
        try:
            if guild_id:
                url = guild_command_url.format(application_id=application_id, command_id=command_id, guild_id=guild_id)
            else:
                url = global_command_url.format(application_id=application_id, command_id=command_id, guild_id=guild_id)

            r = requests.patch(url, headers=headers, json=json.loads(command_json.read()))
            print(r.status_code)
            pprint(r.json())
        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    cli()
