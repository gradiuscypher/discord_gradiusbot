import random
import asyncio

vowels = set('aeiou')

print("[Public Plugin] <giveabitch.py>: This plugin tells you what to give a bitch.")


@asyncio.coroutine
def action(message, client, config):
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
