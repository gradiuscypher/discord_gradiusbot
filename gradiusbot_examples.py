#!venv/bin/python

import discord
import configparser


config = configparser.RawConfigParser()
config.read('config.conf')

username = config.get('Discord', 'username')
password = config.get('Discord', 'password')

client = discord.Client()
client.login(username, password)


@client.event
def on_ready():
    print("Connected")
    print(client.servers)
    print(client.servers[0].channels)


@client.event
def on_message(message):

    print(str(dir(message)))

    if message.channel.is_private:
        print("===== PRIVATE MESSAGE START =====")
        print(message.id)
        print(message.author)
        print(message.content)
        print(message.embeds)
        print(message.attachments)
        print("===== MESSAGE END =====")
        print()

    else:
        print("===== MESSAGE START =====")
        print("ID:", message.id)
        print("SERVER NAME:", message.channel.server.name)

        print("IS_PRIVATE:", message.channel.is_private)
        print("CHANNEL_POSITION:", message.channel.position)
        print("CHANNEL_TOPIC:", message.channel.topic)

        print("AUTHOR:", message.author)
        print("CONTENT:", message.content)
        print("MENTION_EVERYONE:", message.mention_everyone)
        print("EMBEDS:", message.embeds)
        print("ATTACHMENTS:", message.attachments)
        print("===== MESSAGE END =====")
        print()

client.run()
