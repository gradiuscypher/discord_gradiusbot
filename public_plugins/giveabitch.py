import random

vowels = set('aeiou')


def action(message, send_message_callback):
    words = [line.strip() for line in open('data/items.data')]
    gift = random.choice(words).upper()

    plural = pluralize(gift).upper()

    if gift[0] in vowels:
        gift = 'N ' + gift
    else:
        gift = ' ' + gift

    if "what do you give a" in message.content.lower():
        target = message.content.split()[-1].replace('?', '')
        send_message_callback(message.channel, 'GIVE THAT ' + target.upper() + ' A' + gift + '. ' + target.upper() + 'S LOVE ' + plural + '.')


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
