#! venv3/bin/python

import discord
import asyncio
import configparser
import traceback
import json
import logging
import sys

config = configparser.RawConfigParser()
client = discord.Client()


@client.async_event
def on_ready():
    print('Logged in as: ', client.user.name, 'with ID:', client.user.id)


@client.async_event
def on_message(message):
    channel = message.channel
    server = message.server
    author = message.author.name
    content = message.content
    embeds = message.embeds
    attachments = message.attachments

    if len(embeds) > 0:
        print("[on_message +embed] {} {} {}\nm:    {}\n    {}".format(server, channel, author, content, repr(embeds)))

    elif len(attachments) > 0:
        print("[on_message +attach] {} {} {}\nm  :    {}\nfn :    {}\nurl:    {}".format(server, channel, author, content, attachments[0]['filename'], attachments[0]['url']))

    else:
        print("[on_message] {} {} {}\nm:    {}".format(server, channel, author, content))


@client.async_event
def on_message_delete(message):
    channel = message.channel
    server = message.server
    author = message.author.name
    content = message.content
    embeds = message.embeds
    attachments = message.attachments

    if len(embeds) > 0:
        print("[on_message_delete +embed] {} {} {}\nm:    {}\n    {}".format(server, channel, author, content, repr(embeds)))

    elif len(attachments) > 0:
        print("[on_message_delete +attach] {} {} {}\nm  :    {}\nfn :    {}\nurl:    {}".format(server, channel, author, content, attachments[0]['filename'], attachments[0]['url']))

    else:
        print("[on_message_delete] {} {} {}\nm:    {}".format(server, channel, author, content))


@client.async_event
def on_message_edit(before, after):
    channel = before.channel
    server = before.server
    author = before.author.name
    bcontent = before.content
    acontent = after.content
    print("[on_message_edit] {} - {} - {}\n-    {}\n+    {}".format(server, channel, author, bcontent, acontent))


@client.async_event
def on_reaction_add(reaction, user):
    author = user.name
    count = reaction.count
    message = reaction.message.content

    if not reaction.custom_emoji:
        emoji = reaction.emoji
        print("[on_reaction_add] {}:{}\n+    {} [{}]".format(author, message, emoji, count))
    else:
        emoji = reaction.emoji.name
        print("[on_reaction_add] {}:{}\n+    {} [{}]".format(author, message, emoji, count))


@client.async_event
def on_reaction_remove(reaction, user):
    author = user.name
    count = reaction.count
    message = reaction.message.content

    if not reaction.custom_emoji:
        emoji = reaction.emoji
        print("[on_reaction_remove] {}:{}\n-    {} [{}]".format(author, message, emoji, count))
    else:
        emoji = reaction.emoji.name
        print("[on_reaction_remove] {}:{}\n-    {} [{}]".format(author, message, emoji, count))


@client.async_event
def on_member_join(member):
    username = member.name
    print("[on_member_join] {}".format(username))


@client.async_event
def on_member_remove(member):
    username = member.name
    print("[on_member_remove] {}".format(username))


def main_task(config_file):
    config.read(config_file)
    token = config.get("Account", "token")

    if config.getboolean("BotSettings", "debug"):
        logging.basicConfig(level=logging.DEBUG)

    if config.getboolean("BotSettings", "logfile"):
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)


    try:
        print("Running client...")
        client.run(token)
    except KeyboardInterrupt:
        print("Killed by keboard!")
    except:
        print("There was an exception:")
        print(traceback.print_exc())


if __name__ == "__main__":
    main_task(sys.argv[1])
