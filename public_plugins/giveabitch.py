# Config options: ("giveabitch", "time_limit"), ("giveabitch", "permitted_channels")

from libs.ratelimiter import Ratelimiter
import random
import asyncio
import json

vowels = set('aeiou')
rl = Ratelimiter()

print("[Public Plugin] <giveabitch.py>: This plugin tells you what to give a bitch.")

help_message = """
__**give a bitch help**__
Tells you what to give a bitch. Just ask the question, "what do you give a X?" where X is replaced by what you want to know.
"""


@asyncio.coroutine
def action(message, client, config):

    if config.has_option("giveabitch", "time_limit"):
        time_limit = config.getint("giveabitch", "time_limit")
    else:
        time_limit = 60

    if config.has_option("giveabitch", "permitted_channels"):
        permitted_channels = json.loads(config.get('giveabitch', 'permitted_channels'))
    else:
        permitted_channels = []

    if message.channel.name in permitted_channels:
        if not rl.is_rate_limited(message.author.id, "giveabitch", time_limit):
            words = [line.strip() for line in open('data/items.data')]
            gift = random.choice(words).upper()

            plural = pluralize(gift).upper()

            if gift[0] in vowels:
                gift = 'N ' + gift
            else:
                gift = ' ' + gift

            if "what do you give a " in message.content.lower():
                split_message = message.content.lower().split('what do you give a ')

                if len(split_message) > 1:
                    target = split_message[-1].replace('?', '')
                    yield from client.send_message(message.channel, 'GIVE THAT ' + target.upper() + ' A' + gift + '. ' + target.upper() + 'S LOVE ' + plural + '.')


def pluralize(singular):
    root = singular
    try:
        if singular[-1] == 'y' and singular[-2] not in vowels:
            root = singular[:-1]
            suffix = 'ies'
        elif singular[-1] == 's':
            if singular[-2] in vowels:
                if singular[-3:] == 'ius':
                    root = singular[:-2]
                    suffix = 'i'
                else:
                    root = singular[:-1]
                    suffix = 'ses'
            else:
                suffix = 'es'
        elif singular[-2:] in ('ch', 'sh'):
            suffix = 'es'
        else:
            suffix = 's'
    except IndexError:
        suffix = 's'
    plural = root + suffix
    return plural
